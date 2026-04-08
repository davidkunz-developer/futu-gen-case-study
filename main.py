import asyncio
import io
import os
import tempfile
import threading
from contextlib import asynccontextmanager
from typing import Optional

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

load_dotenv()

from functions import (
    mock_audio_streamer,
    live_mic_streamer,
    transcription_engine_worker,
    speaker_diarization_worker,
    record_compiler_worker_broadcasting,
    llm_classifier_worker,
)

# Queues with maxsize to prevent memory accumulation
whisper_queue = asyncio.Queue(maxsize=2)
diarization_queue = asyncio.Queue(maxsize=2)
whisper_out_queue = asyncio.Queue()
diar_out_queue = asyncio.Queue()
broadcaster_queue = asyncio.Queue()
classifier_queue = asyncio.Queue()

# Application state
pipeline_tasks: set[asyncio.Task] = set()
intake_task: Optional[asyncio.Task] = None
connected_clients: set[WebSocket] = set()

async def broadcast_manager(queue: asyncio.Queue):
    """Broadcasting messages to all connected WebSocket clients."""
    while True:
        event = await queue.get()
        if hasattr(event, "model_dump"):
            payload = event.model_dump()
        else:
            payload = event
            
        dead = set()
        for client in list(connected_clients):
            try:
                await client.send_json(payload)
            except Exception:
                dead.add(client)
        for d in dead:
            connected_clients.discard(d)
        queue.task_done()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan manager for backend tasks startup and shutdown."""
    print("Backend starting - waiting for stream command...")

    # Initialize workers
    pipeline_tasks.add(asyncio.create_task(transcription_engine_worker(whisper_queue, whisper_out_queue)))
    pipeline_tasks.add(asyncio.create_task(speaker_diarization_worker(diarization_queue, diar_out_queue)))
    pipeline_tasks.add(asyncio.create_task(record_compiler_worker_broadcasting(whisper_out_queue, diar_out_queue, [broadcaster_queue, classifier_queue])))
    pipeline_tasks.add(asyncio.create_task(llm_classifier_worker(classifier_queue, broadcaster_queue)))
    pipeline_tasks.add(asyncio.create_task(broadcast_manager(broadcaster_queue)))

    yield

    print("Shutting down backend.")
    for t in pipeline_tasks:
        t.cancel()
    if intake_task and not intake_task.done():
        intake_task.cancel()

app = FastAPI(lifespan=lifespan, title="FutuGen Audio Pipeline")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def _clear_queues():
    """Clears all queues before a new recording starts."""
    for q in [whisper_queue, diarization_queue, whisper_out_queue, diar_out_queue, broadcaster_queue, classifier_queue]:
        while not q.empty():
            try:
                q.get_nowait()
            except Exception:
                pass

async def _stop_intake():
    """Stops the current audio intake task."""
    global intake_task
    if intake_task and not intake_task.done():
        print("[Intake] Stopping current task...")
        intake_task.cancel()
        try:
            await asyncio.wait_for(intake_task, timeout=2.0)
        except (asyncio.CancelledError, asyncio.TimeoutError):
            pass
    intake_task = None

@app.post("/api/start/mock")
async def start_mock():
    """Starts mock streaming from wav file."""
    global intake_task
    await _stop_intake()
    _clear_queues()
    intake_task = asyncio.create_task(
        mock_audio_streamer("mock.wav", "SESS-001", [whisper_queue, diarization_queue])
    )
    print("[Intake] MOCK mode started (mock.wav)")
    return {"status": "started", "mode": "mock"}

@app.post("/api/start/mic")
async def start_mic():
    """Starts live streaming from microphone."""
    global intake_task
    await _stop_intake()
    _clear_queues()
    intake_task = asyncio.create_task(
        live_mic_streamer("SESS-001", [whisper_queue, diarization_queue])
    )
    print("[Intake] LIVE MIC mode started")
    return {"status": "started", "mode": "mic"}

@app.post("/api/start/upload")
async def start_upload(file: UploadFile = File(...)):
    """Starts streaming from uploaded wav file."""
    global intake_task
    await _stop_intake()
    _clear_queues()

    contents = await file.read()
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    tmp.write(contents)
    tmp.close()

    intake_task = asyncio.create_task(
        mock_audio_streamer(tmp.name, "SESS-001", [whisper_queue, diarization_queue])
    )
    print(f"[Intake] UPLOAD mode started ({file.filename})")
    return {"status": "started", "mode": "upload", "filename": file.filename}

@app.post("/api/stop")
async def stop_stream():
    """Stops the current streaming session."""
    await _stop_intake()
    print("[Intake] Stream stopped.")
    return {"status": "stopped"}

@app.get("/")
async def status():
    """Returns current system status."""
    return {
        "status": "running",
        "clients": len(connected_clients),
        "intake_running": intake_task is not None and not intake_task.done(),
    }

@app.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    """Internal WebSocket endpoint for real-time data broadcasting."""
    await websocket.accept()
    connected_clients.add(websocket)
    print(f"[WS] Client connected. Total: {len(connected_clients)}")
    try:
        while True:
            await asyncio.sleep(1.0)
    except WebSocketDisconnect:
        connected_clients.discard(websocket)
        print(f"[WS] Client disconnected. Total: {len(connected_clients)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
