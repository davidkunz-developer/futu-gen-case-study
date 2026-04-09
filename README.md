# FutuGen - Audio Streaming & AI Klasifikační Pipeline

Tento projekt implementuje kompletní asynchronní pipeline pro zpracování audio streamů, transkripci v reálném čase (STT) a inteligentní klasifikaci konverzací.

## Hlavní funkce
- **Streaming v reálném čase**: Podpora pro vstup z mikrofonu, nahrávání souborů a simulovaný (Mock) stream.
- **Deepgram Nova-2 Engine**: Vysoce výkonná česká transkripce s latencí pod jednu sekundu.
- **Integrovaná diarizace**: Automatické rozlišení mluvčích (S1, S2...) přímo v rámci streamu.
- **Inkrementální klasifikace**: Analýza v reálném čase (Soukromé vs. Tématické) pomocí GPT-4o-mini.
- **Moderní UI**: Dashboard v Reactu (Vite) pro vizualizaci dat v reálném čase.

## Architektura
Systém využívá `asyncio` a skládá se ze tří hlavních modulů:
1. **Audio Streamer**: Zajišťuje příjem audio dat, normalizaci (16kHz Mono) a rozdělení na části.
2. **Transcription Engine**: Integruje Deepgram WebSocket pro paralelní transkripci a diarizaci.
3. **Classifier**: Průběžná analýza textu pomocí posuvného okna (sliding-window) s výstupem ve strukturovaném JSONu.

### Volba technologie: Deepgram Nova-2 vs. OpenAI Whisper
Ačkoliv původní zadání zmiňovalo OpenAI Whisper, naše architektonická analýza upřednostnila **Deepgram Nova-2** pro tento konkrétní real-time use case. Hlavní důvody:

1. **Latence pod sekundu**: API OpenAI Whisper (založené na REST) vyžaduje nahrávání delších audio úseků, což vede k výraznému zpoždění. Deepgram využívá kontinuální WebSocket stream, což umožňuje latenci pod 500ms.
2. **Streamingová diarizace**: Deepgram poskytuje nativní separaci mluvčích přímo ve výsledcích živého streamu. U Whisperu by to vyžadovalo další post-processing (např. Pyannote), což narušuje zážitek z reálného času.
3. **Pokročilá podpora více kanálů**: Naše implementace podporuje pravé stereo, kde mapujeme levý/pravý kanál přímo na ID mluvčích – funkce, která u běžných implementací Whisperu pro streaming chybí.

**Poznámka k modularitě**: Architektura systému je plně modulární. Pokud by požadavky striktně vyžadovaly OpenAI Whisper, lze `transcription_engine_worker` ve `functions.py` snadno vyměnit. Pro účely této případové studie byl však zvolen Deepgram, aby demonstroval špičkové řešení s nejnižší latencí, které přesahuje základní požadavky.

## Instalace a nastavení

### Požadavky
- Python 3.10+
- Node.js (pro frontend)
- API klíče v souboru `.env` (Deepgram, OpenAI)

### Lokální spuštění (Nativní)
Pro plnou funkčnost včetně mikrofonu doporučujeme nativní běh:

#### Backend
```bash
python -m venv venv
# Aktivace na Windows:
.\venv\Scripts\activate 
pip install -r requirements.txt
python main.py
```

#### Frontend (volitelně samostatně)
```bash
cd frontend
npm install
npm run dev
```

## Evaluace a testování
Projekt obsahuje evaluační sadu 10 konverzací s referenčními popisky.
Pro spuštění testu přesnosti:
```bash
python tests/eval_script.py
```

## Docker & Deployment
Aplikace je plně kontejnerizovaná a připravená pro nasazení (např. na Render).

### Sestavení a spuštění
```bash
docker build -t futugen-app .
docker run -d --name futugen -p 8000:8000 --env-file .env futugen-app
```
Aplikace bude dostupná na: `http://localhost:8000` (FastAPI + Integrovaný React Frontend).

### ⚠️ Důležité omezení (Mikrofon v Dockeru)
Při běhu v Dockeru **není možné** přistupovat k fyzickému mikrofonu vašeho hostitelského počítače z backendu (chybí audio passthrough). 

**Pro otestování funkčnosti v Dockeru:**
1. Klikněte na tlačítko **"Mock Stream"** – spustí se simulace z přiloženého WAV souboru.
2. Klikněte na **"WAV File"** – nahrajte vlastní audio soubor.

**Pro nahrávání z mikrofonu:**
Musíte aplikaci spustit **nativně** (mimo Docker) podle instrukcí výše.

---
**Autor:** David Kunz (FutuGen AI Team)
**Stav:** Připraveno k odevzdání
