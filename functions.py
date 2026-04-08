import os
import asyncio
import base64
import json
import time
import uuid
import numpy as np
from typing import List, Optional, Set
from pydantic import BaseModel
from dotenv import load_dotenv

from models import AudioChunk, TranscriptionRecord, ClassificationResult, AudioWord
from deepgram import (
    DeepgramClient,
    LiveTranscriptionEvents,
    LiveOptions,
    DeepgramClientOptions,
)

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

def resample_audio(audio_bytes: bytes, from_rate: int, to_rate: int, num_channels: int = 1) -> bytes:
    """Resamples audio bytes to a target sample rate (preserving channels)."""
    audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32)
    
    if from_rate == to_rate: 
        return audio_np.astype(np.int16).tobytes()
        
    num_samples = int((len(audio_np) // num_channels) * to_rate / from_rate)
    
    if num_channels == 1:
        resampled_np = np.interp(
            np.linspace(0, len(audio_np), num_samples, endpoint=False),
            np.arange(len(audio_np)),
            audio_np
        )
    else:
        # Resample each channel separately
        reshaped = audio_np.reshape(-1, num_channels)
        resampled_channels = []
        for i in range(num_channels):
            resampled_channels.append(np.interp(
                np.linspace(0, len(reshaped), num_samples, endpoint=False),
                np.arange(len(reshaped)),
                reshaped[:, i]
            ))
        resampled_np = np.vstack(resampled_channels).T.flatten()
        
    return resampled_np.astype(np.int16).tobytes()

async def mock_audio_streamer(wav_path: str, session_id: str, queues: List[asyncio.Queue]):
    """Simulates an audio stream from a WAV file."""
    import wave
    try:
        with wave.open(wav_path, 'rb') as wf:
            native_sr = wf.getframerate()
            n_channels = wf.getnchannels()
            chunk_duration_s = 2.0
            chunk_size_native = int(native_sr * chunk_duration_s)
            print(f"[Mock] Starting: {wav_path} ({native_sr}Hz, {n_channels}ch -> 16000Hz, mono)")
            chunk_idx = 0
            while True:
                data = wf.readframes(chunk_size_native)
                if not data: 
                    print("[Mock] End of file reached.")
                    break
                data_16k = resample_audio(data, native_sr, 16000, n_channels)
                
                chunk = AudioChunk(
                    session_id=session_id,
                    timestamp_start=chunk_idx * chunk_duration_s,
                    timestamp_end=(chunk_idx + 1) * chunk_duration_s,
                    sample_rate=16000,
                    duration_ms=int(chunk_duration_s * 1000),
                    audio_data=base64.b64encode(data_16k).decode('utf-8')
                )
                
                print(f"[Mock] Sending chunk {chunk_idx} to queues...")
                for q in queues:
                    try: q.put_nowait(chunk)
                    except Exception as e: print(f"[Mock] Queue error: {e}")
                chunk_idx += 1
                await asyncio.sleep(chunk_duration_s)
    except Exception as e:
        print(f"[Mock] Error: {e}")

async def live_mic_streamer(session_id: str, queues: List[asyncio.Queue]):
    """Streams live audio from the default microphone."""
    import pyaudio
    p = pyaudio.PyAudio()
    TARGET_RATE = 16000
    INPUT_RATE = 16000
    try:
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=INPUT_RATE, input=True, frames_per_buffer=INPUT_RATE)
    except:
        INPUT_RATE = 44100
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=INPUT_RATE, input=True, frames_per_buffer=INPUT_RATE)
    
    print(f"[Mic] Streaming: {INPUT_RATE}Hz -> {TARGET_RATE}Hz")
    chunk_idx = 0
    try:
        while True:
            data = await asyncio.to_thread(stream.read, INPUT_RATE, exception_on_overflow=False)
            data_16k = resample_audio(data, INPUT_RATE, TARGET_RATE, 1)
            
            chunk = AudioChunk(
                session_id=session_id,
                timestamp_start=chunk_idx * 1.0,
                timestamp_end=(chunk_idx + 1) * 1.0,
                sample_rate=16000,
                duration_ms=1000,
                audio_data=base64.b64encode(data_16k).decode('utf-8')
            )
            for q in queues:
                try: q.put_nowait(chunk)
                except: pass
            chunk_idx += 1
    except asyncio.CancelledError:
        print("[Mic] Stopped.")
    finally:
        try:
            stream.stop_stream()
            stream.close()
        except: pass
        p.terminate()

async def transcription_engine_worker(in_queue: asyncio.Queue, out_queue: asyncio.Queue):
    """Deepgram-based transcription worker with integrated diarization."""
    if not DEEPGRAM_API_KEY: 
        print("[DG Worker] CRITICAL: API key missing!")
        return
    client = DeepgramClient(DEEPGRAM_API_KEY)
    dg_connection = None
    dg_current_channels = None
    loop = asyncio.get_event_loop()
    
    current_session_id = None
    latest_chunk_id = "CHK-LIVE"

    def on_message(self, result, **kwargs):
        try:
            if not result.is_final: return
            if not result.channel.alternatives: return
            alt = result.channel.alternatives[0]
            if not alt.transcript: return
            
            # Speaker ID mapping
            # Pokud máme více kanálů (Stereo), bereme S1/S2 z indexu kanálu.
            # Pokud máme jen jeden kanál (Mono Mic), vracíme se k diarizaci z Deepgramu.
            channel_idx = getattr(result, 'channel_index', [0])[0]
            speaker = 0
            
            if dg_current_channels > 1:
                speaker = channel_idx
            elif alt.words:
                # Majority vote diarizace pro Mono
                speaker_counts = {}
                for w in alt.words:
                    s = getattr(w, 'speaker', getattr(w, 'speaker_index', 0))
                    speaker_counts[s] = speaker_counts.get(s, 0) + 1
                if speaker_counts:
                    speaker = max(speaker_counts, key=speaker_counts.get)
            
            speaker_id = f"S{speaker + 1}"
            
            audio_words = []
            for w in alt.words:
                audio_words.append(AudioWord(word=w.word, start=w.start, end=w.end))
            
            rec = TranscriptionRecord(
                chunk_id=latest_chunk_id,
                session_id=current_session_id,
                speaker_id=speaker_id,
                text=alt.transcript,
                language="cs",
                timestamp_start=result.start,
                timestamp_end=result.start + result.duration,
                confidence=alt.confidence,
                words=audio_words
            )
            
            print(f"[DG] {rec.speaker_id} (ch:{channel_idx}): {rec.text}")
            loop.call_soon_threadsafe(out_queue.put_nowait, rec)
        except Exception as e: 
            print(f"[DG Callback] Error: {e}")

    def start_dg(channels: int = 1):
        print(f"[DG Worker] Initializing Deepgram ({channels} ch, High-Stability Mode)...")
        try:
            conn = client.listen.live.v("1")
            conn.on(LiveTranscriptionEvents.Transcript, on_message)
            conn.on(LiveTranscriptionEvents.Error, lambda s, e, **kw: print(f"[DG] Global Error: {e}"))
            options = LiveOptions(
                model="nova-2", 
                language="cs", 
                smart_format=True,
                punctuate=True,
                diarize=True, 
                multichannel=(channels > 1),
                channels=channels,
                no_delay=True,
                encoding="linear16", 
                sample_rate=16000,
                interim_results=True,
                utterance_end_ms=1000
            )
            if conn.start(options) is False: 
                print("[DG Worker] Failed to start connection.")
                return None
            return conn
        except Exception as e:
            print(f"[DG Worker] Connection crash: {e}")
            return None

    try:
        while True:
            chunk: AudioChunk = await in_queue.get()
            
            # Detekce kanálů
            raw_audio = base64.b64decode(chunk.audio_data)
            n_samples_total = len(raw_audio) // 2
            detected_channels = int(round(n_samples_total / (16000 * (chunk.duration_ms / 1000))))
            if detected_channels < 1: detected_channels = 1
            
            # Restart hovoru při změně ID relace nebo počtu kanálů
            if current_session_id != chunk.session_id or dg_current_channels != detected_channels:
                if dg_connection: 
                    print(f"[DG Worker] Resetting connection (New Session or Channel Change: {dg_current_channels}->{detected_channels})")
                    dg_connection.finish()
                dg_connection = start_dg(channels=detected_channels)
                current_session_id = chunk.session_id
                dg_current_channels = detected_channels
            
            latest_chunk_id = chunk.chunk_id

            if not dg_connection:
                in_queue.task_done()
                continue
            
            try:
                dg_connection.send(raw_audio)
            except Exception as e:
                print(f"[DG Worker] Send error: {e}. Retrying...")
                dg_connection = start_dg(channels=detected_channels)
                if dg_connection: dg_connection.send(raw_audio)
            in_queue.task_done()
    except asyncio.CancelledError: pass
    finally:
        if dg_connection: dg_connection.finish()

async def record_compiler_worker_broadcasting(win_q: asyncio.Queue, diar_q: asyncio.Queue, out_qs: List[asyncio.Queue]):
    """Aggregates transcription records and broadcasts them to multiple output queues."""
    while True:
        rec: TranscriptionRecord = await win_q.get()
        try:
            with open("log_transcription.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(rec.model_dump(), ensure_ascii=False) + "\n")
        except: pass
        for q in out_qs: await q.put(rec)
        win_q.task_done()

async def llm_classifier_worker(in_queue: asyncio.Queue, out_queue: asyncio.Queue):
    """LLM-based incremental classification worker using sliding window context."""
    from openai import AsyncOpenAI
    openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    from prompts import CLASSIFIER_SYSTEM_PROMPT
    
    history_buffer = []
    last_analysis_time = 0
    start_time = time.time()
    
    while True:
        record: TranscriptionRecord = await in_queue.get()
        history_buffer.append(record)
        
        current_time = time.time()
        if len(history_buffer) >= 5 and (current_time - last_analysis_time > 10):
            context_lines = [f"{r.speaker_id}: {r.text}" for r in history_buffer[-20:]]
            context = "\n".join(context_lines)
            unique_speakers = len(set(r.speaker_id for r in history_buffer[-20:]))
            
            try:
                response = await openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": CLASSIFIER_SYSTEM_PROMPT},
                        {"role": "user", "content": f"Participants: {unique_speakers}. Context:\n\n{context}"}
                    ],
                    response_format={"type": "json_object"}
                )
                raw_payload = json.loads(response.choices[0].message.content)
                
                result = ClassificationResult(
                    session_id=record.session_id,
                    classification=raw_payload.get("classification", "topic_based"),
                    confidence=raw_payload.get("confidence", 0.0),
                    topics=raw_payload.get("topics", []),
                    privacy_signals=raw_payload.get("privacy_signals", []),
                    dominant_topic=raw_payload.get("dominant_topic", ""),
                    sentiment=raw_payload.get("sentiment", "neutral"),
                    participants_count=unique_speakers,
                    total_duration_s=round(time.time() - start_time, 1),
                    model_used="deepgram-nova2 + gpt-4o-mini"
                )
                
                await out_queue.put(result)
                last_analysis_time = time.time()
                print(f"[Classifier] Result: {result.classification}")
            except Exception as e:
                print(f"[Classifier] Error: {e}")
        
        in_queue.task_done()

async def speaker_diarization_worker(in_queue: asyncio.Queue, out_queue: asyncio.Queue):
    """Placeholder for modular diarization (currently handled by Deepgram)."""
    while True:
        await in_queue.get()
        in_queue.task_done()
