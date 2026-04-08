import pytest
import asyncio
from fastapi.testclient import TestClient
from main import app, whisper_queue, diarization_queue
from models import AudioChunk, TranscriptionRecord, ClassificationResult

client = TestClient(app)

@pytest.mark.asyncio
async def test_health_check_endpoint():
    """Verify API server is running and returning correct status."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "running"

@pytest.mark.asyncio
async def test_payload_validation_audio_chunk():
    """Verify Pydantic validation for AudioChunk model."""
    chunk = AudioChunk(
        chunk_id="chk-001",
        session_id="SESS-000",
        audio_data="BASE64MOCK=",
        timestamp_start=2.5,
        timestamp_end=5.0,
        sample_rate=16000,
        duration_ms=2500
    )
    assert chunk.duration_ms == 2500
    assert chunk.timestamp_end > chunk.timestamp_start

@pytest.mark.asyncio
async def test_payload_validation_transcription():
    """Verify Pydantic validation for TranscriptionRecord model."""
    record = TranscriptionRecord(
        chunk_id="chk-001",
        session_id="SESS-000",
        speaker_id="SPEAKER_00",
        text="Dobrý den, tady je test.",
        language="cs",
        timestamp_start=2.5,
        timestamp_end=5.0,
        confidence=0.98
    )
    assert record.speaker_id == "SPEAKER_00"
    assert "test" in record.text
    assert record.record_id is not None

@pytest.mark.asyncio
async def test_payload_validation_classification():
    """Verify Pydantic validation for ClassificationResult model."""
    classification = ClassificationResult(
        session_id="SESS-000",
        classification="private",
        confidence=0.99,
        topics=["testing", "architecture"],
        dominant_topic="architecture",
        sentiment="neutral",
        participants_count=2,
        total_duration_s=5.0
    )
    assert classification.classification in ["private", "topic_based"]
    assert len(classification.topics) == 2

@pytest.mark.asyncio
async def test_websocket_endpoint_connection():
    """Verify WebSocket endpoint connectivity."""
    with client.websocket_connect("/ws/stream") as websocket:
        assert websocket is not None

@pytest.mark.asyncio
async def test_async_queue_transmission():
    """Verify basic asyncio queue operations."""
    q1 = asyncio.Queue()
    q2 = asyncio.Queue()
    
    await q1.put("msg1")
    await q2.put("msg2")
    
    assert q1.qsize() == 1
    assert await q1.get() == "msg1"
    assert q2.qsize() == 1
