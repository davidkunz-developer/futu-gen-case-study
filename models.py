from pydantic import BaseModel, Field
from typing import List, Optional
import uuid

class AudioWord(BaseModel):
    word: str
    start: float
    end: float

class AudioChunk(BaseModel):
    """Base64 audio chunk with metadata."""
    chunk_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    timestamp_start: float
    timestamp_end: float
    sample_rate: int
    duration_ms: int
    audio_data: str

class TranscriptionRecord(BaseModel):
    """Structured transcription record matching requirements."""
    record_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    chunk_id: str
    session_id: str
    speaker_id: Optional[str] = None
    text: str
    language: str = "cs"
    timestamp_start: float
    timestamp_end: float
    confidence: float
    words: Optional[List[AudioWord]] = None

class ClassificationResult(BaseModel):
    """AI classification result matching requirements."""
    session_id: str
    classification: str
    confidence: float
    topics: List[str]
    privacy_signals: Optional[List[str]] = None
    dominant_topic: str
    sentiment: str
    participants_count: int
    total_duration_s: float
    model_used: str = "deepgram-nova2 + gpt-4o-mini"
