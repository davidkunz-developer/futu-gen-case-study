# FutuGen - Audio Streaming & AI Classification Pipeline

This project implements a complete asynchronous pipeline for processing audio streams, real-time transcription (STT), and intelligent conversation classification.

## Core Features
- **Real-time Streaming**: Support for microphone input, file upload, and simulated (Mock) stream.
- **Deepgram Nova-2 Engine**: High-performance Czech transcription with sub-second latency.
- **Integrated Diarization**: Automatic speaker separation (S1, S2...) within the stream.
- **Incremental Classification**: Real-time analysis (Private vs. Topic-Based) using GPT-4o-mini.
- **Modern UI**: React (Vite) dashboard for real-time visualization.

## Architecture
The system uses `asyncio` and consists of three main modules:
1. **Audio Streamer**: Handles intake, normalization (16kHz Mono), and chunking.
2. **Transcription Engine**: Integrates Deepgram WebSocket for parallel transcription and diarization.
3. **Classifier**: Sliding-window text analysis producing structured JSON output.

### Technology Choice: Deepgram Nova-2 vs. OpenAI Whisper
While the initial project requirements mentioned OpenAI Whisper, our architectural analysis favored **Deepgram Nova-2** for this specific real-time use case. Key reasons include:

1. **Sub-second Latency**: OpenAI's Whisper API (REST-based) requires multi-second audio segments to be uploaded, leading to significant chunking delays. Deepgram uses a constant WebSocket stream, allowing for sub-500ms end-to-end latency.
2. **Streaming Diarization**: Deepgram provides native speaker diarization within its live streaming results. Achieving this with Whisper would require an additional post-processing step (like Pyannote), which breaks the real-time experience.
3. **Advanced Multichannel Support**: Our implementation supports true stereo input, mapping left/right channels directly to speaker IDs—a feature not natively supported by streaming Whisper implementations.

**Note on Modularity**: The system architecture is fully modular. Should the project requirements strictly mandate OpenAI Whisper, the `transcription_engine_worker` in `functions.py` can be easily swapped back. However, for the purpose of this case study, Deepgram was chosen to demonstrate a production-grade, lowest-latency solution that exceeds the baseline requirements.

## Installation and Setup

### Prerequisites
- Python 3.10+
- Node.js (frontend)
- API keys in `.env` (Deepgram, OpenAI)

### Backend
```bash
python -m venv venv
source venv/bin/activate  # venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Evaluation and Testing
Includes an evaluation dataset of 10 conversations with ground truth labels.
To run the accuracy test:
```bash
python tests/eval_script.py
```

## Docker
Includes `docker-compose.yml` for backend deployment.
```bash
docker-compose up --build
```

---
**Author:** David Kunz (FutuGen AI Team)
**Status:** Ready for Review
