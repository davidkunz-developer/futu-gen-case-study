# System Requirements: FutuGen Audio Classification Pipeline

## 1. Technologický Stack
- **Jazyk:** Python 3.10+
- **Asynchronní model:** `asyncio` pro kompletní neblokující provoz
- **Transkripční model:** OpenAI Whisper API / **Deepgram Nova-2** (Cílená výjimka pro real-time latenci)
- **Diarizace:** **Deepgram Integrated** (Smluvní výjimka z lokálního Pyannote pro snížení CPU režie)
- **Klasifikátor (LLM):** OpenAI API (`gpt-4o-mini`)
- **WebSockets / API:** `FastAPI` + `websockets`
- **Typování & Validace:** `pydantic`
- **Konfigurace & Zázemí:** `python-dotenv`, Docker Compose

## 2. Funkční Požadavky

### Modul 1: Audio Streaming Layer
- **Zdroje vstupu:** 
  1. Mock Mode (čte existující wav soubor po kouscích).
  2. Live Mode (simulovaný/reálný PyAudio stream).
- **Chunkování:** Deepgram Streaming nevyžaduje velké překryvy, stačí plynulé feedování audio dat.
- **Normalizace:** Vše se na výstupu převede interně pod 16kHz Mono.

### Modul 2: Transcription & Diarization Engine (Integrated)
- Audio stream je odesílán přímo na Deepgram WebSocket.
- **Diarizace:** Vrací se v reálném čase jako součást transkripčního objektu.
- **Záznam do JSONL:** Engine appenduje každý finální přepsaný block do repozitářového `.jsonl` záznamu.

### Modul 3: Klasifikátor
- Běží v samostatné cyklické smyčce (Inkrementální klasifikace - Bonus).
- Načítá posledních $N$ záznamů (sliding window textu) a odesílá prompt na LLM (Gemini API).
- LLM prompt vynucuje strukturovaný JSON výstup rozlišující "Private" vs "Topic-Based".

### Modul 4: Integrace & WebSockets (Bonus)
- Všechny eventy (Transkripce, Změna Mluvčího, Aktualizace Klasifikátorů) se asynchronně broadcastují skrze FastAPI WebSocket připojeným klientům (simulace Live Vieweru).

## 3. Akceptační Kritéria (Bonusy splněny)
1. Kód je spustitelný skrz jednoduchý `docker-compose up` nebo aspoň rozdělený na jasné služby.
2. Jde o 100% asynchronní chain (pipeline queues).
3. Splněna Inkrementální klasifikace LLM.
4. Přítomen je Evaluační / Testovací skript v Pytestu (`pytest tests/`).
