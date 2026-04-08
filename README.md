# FutuGen - Real-time Audio Diarization & Classification Pipeline

Tento projekt implementuje vysoce výkonnou pipeline pro reálný čas, která zpracovává audio stream (mikrofon nebo soubor), provádí transkripci s rozlišením mluvčích (diarizace) a následně text klasifikuje pomocí LLM (detekce tématu a soukromých údajů).

## Hlavní Funkce
- **Nízká Latence**: Pod-sekundová odezva díky Deepgram Nova-2 WebSocket streamingu.
- **Hybridní Diarizace**: Automatické rozlišení mluvčích S1/S2/S3... pro Mono i Stereo vstupy.
- **Inkrementální Klasifikace**: Analýza textu v reálném čase (Téma vs. Soukromé údaje) pomocí GPT-4o-mini.
- **Moderní UI**: Dashboard v Reactu (Vite) pro vizualizaci dat a ovládání zdroje zvuku.

## Architektura a Design
Projekt dodržuje princip **Separation of Concerns (SoC)** pro zajištění udržitelnosti:

1. **`main.py` (Orchestrátor)**: Vstupní bod FastAPI serveru. Spravuje WebSocket spojení a asynchronní workery.
2. **`functions.py` (Motor)**: Jádro logiky pro zpracování audia, Deepgram STT a resamplování.
3. **`models.py` (Schéma)**: Definice datových modelů (Pydantic), které sdílí Backend, Frontend i Evaluace.
4. **`prompts.py` (Mozek)**: Centrální úložiště systémových promptů pro LLM klasifikaci.

### Workflow Pipeline
Audio Intake ➔ Whisper Queue ➔ Transcription Engine ➔ Broadcast Queue ➔ LLM Classifier ➔ Frontend

## Technologické rozhodnutí: Deepgram vs. OpenAI Whisper
I když zadání zmiňovalo OpenAI Whisper, zvolili jsme **Deepgram Nova-2** z těchto důvodů:
1. **Rychlost**: Whisper API vyžaduje chunkování a nahrávání celých bloků, což vytváří lag několik sekund. Deepgram streamuje neustále s latencí pod 500ms.
2. **Diarizace**: Deepgram nabízí nativní diarizaci přímo v streamu. S Whisperem by bylo nutné zapojit další model (např. Pyannote), což by latenci ještě zvýšilo.
3. **Stereo Podpora**: Naše implementace plně využívá stereo kanály pro perfektní oddělení operátora a klienta.

**Poznámka k modularitě**: Systém je plně modulární. Pokud by bylo striktně vyžadováno OpenAI Whisper, lze `transcription_engine_worker` v `functions.py` snadno vyměnit.

## Instalace a Spuštění

### Prerekvizity
- Python 3.10+
- Node.js & npm
- API klíče pro Deepgram a OpenAI

### Nastavení
1. Vytvořte `.env` soubor podle `.env.example`:
```env
OPENAI_API_KEY=vaš_klíč
DEEPGRAM_API_KEY=vaš_klíč
```
2. Instalace závislostí:
```bash
pip install -r requirements.txt
```

### Spuštění
**Backend:**
```bash
python main.py
```
**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Evaluace
Pro ověření kvality pipeline je k dispozici suite v adresáři `tests/`:
```bash
python tests/eval_script.py
```
Testuje latenci, přesnost diarizace a klasifikaci na demo datasetu.
