# Datové Schéma & API Contract
Následující struktury jsou formální datové kontrakty mezi moduly navrženého pipelineu. Při vývoji se doporučuje využít `Pydantic BaseModel` (v případě Pythonu) pro validaci a instanciaci během přenosu do Async Front.

---

### 1. AudioChunk
**Producent:** `audio_intake`
**Konzument:** `transcription_engine`, `speaker_diarization`

Struktura reprezentující jeden kousek audio streamu připravený k transkripci.

```json
{
  "chunk_id": "uuid-v4",
  "session_id": "string",
  "timestamp_start": 1700000000.000,
  "timestamp_end": 1700000002.500,
  "sample_rate": 16000,
  "duration_ms": 2500,
  "audio_data": "base64_encoded_pcm"
}
```

---

### 2. TranscriptionRecord
**Producent:** `record_compiler` (na základě dat z Whisperu)
**Konzument:** Zápis do `.jsonl` souboru, `llm_classifier`, `event_broadcaster`

Zkompletovaný log textu obohacený i o detekci řečníka. Každý objekt tvoří jeden řádek `.jsonl` pro lokální persistenci.

```json
{
  "record_id": "uuid-v4",
  "chunk_id": "ref-to-source-chunk",
  "session_id": "string",
  "speaker_id": "SPEAKER_01",
  "text": "Transkribovaný text segmentu.",
  "language": "cs",
  "timestamp_start": 1700000000.000,
  "timestamp_end": 1700000002.500,
  "confidence": 0.94,
  "words": [
     {"word": "Transkribovaný", "start": 0.0, "end": 0.6}
  ]
}
```

---

### 3. ClassificationResult
**Producent:** `llm_classifier`
**Konzument:** `event_broadcaster`

Analýza dodaná jako strukturovaný JSON přímo přes OpenAI API (gpt-4o-mini) LLM model nad sliding window datasetem.

```json
{
  "session_id": "string",
  "classification": "private", 
  "confidence": 0.87,
  "topics": ["technologie", "AI", "rozpočet"],
  "privacy_signals": ["osobní jméno", "adresa"], 
  "dominant_topic": "AI implementace",
  "sentiment": "neutral",
  "participants_count": 2,
  "total_duration_s": 187.4,
  "model_used": "whisper-1 + custom-classifier"
}
```

*Poznámka:* Pole `classification` je Enum formátu (`private` | `topic_based`). Pole `privacy_signals` se použije predikativně jen v případě, že padne klasifikace do "private". Sentiment reflektuje jednu ze tří hodnot (`positive`, `negative`, `neutral`).
