# Backlog - FutuGen Case Study

## Project: Audio Streaming, Transkripce a Klasifikace

**Aktuální Fáze:** 5. Produkční Finalizace & Předání (COMPLETED)

### Kritické opravy (Audit) / Hotovo
- [x] Standardizace na OpenAI API pro transkripci i klasifikaci (@Product-Owner) - **HOTOVO**.
- [x] Oprava signatur a rozbitých volání (`test_stream.py`) (@Tech-Lead) - **HOTOVO**.
- [x] Aktualizace projektové dokumentace (Gemini -> OpenAI) (@Product-Owner) - **HOTOVO**.
- [x] Soulad s JSON schématy v PDF zadání (record_id, confidence, words, privacy_signals) (@Data-Engineer) - **HOTOVO**.

### Zpracovat nyní / Hotovo
- [x] Bonus: FastAPI WebView endpoint pro WebSockets broadcast - Event Broadcaster krabička (Modul 4) (@Backend-Dev) - **HOTOVO** (viz frontend-v2).
- [x] Implementace reálné logiky do `/ws/stream` pro vysílání TranscriptionRecord a ClassificationResult (@Backend-Dev) - **HOTOVO**.
- [x] Implementace Inkrementální klasifikace (Modul 3 Bonus) (@Backend-Dev) - **HOTOVO**.

### Nadcházející iterace / Hotovo
- [x] Zkompletovat `docker-compose.yml` - **HOTOVO**.
- [x] Vytvořit Evaluační sadu (10+ nahrávek) a Eval skript (Bonus Task) - **HOTOVO**.
- [x] Finální README s architekturou a zdůvodněním stacku - **HOTOVO**.

### Hotovo (Done)
- [x] C3: Vývoj Klasifikátoru (krabička `llm_classifier`) přes Gemini/OpenAI API do `functions.py` (Modul 3).
- [x] C2: Vývoj Transcription Engine s Deepgram Nova-2 integrací do `functions.py` (Modul 2).
- [x] C1: Vývoj Audio Streamer Component a vytvoření orchestrátoru `main.py` (Modul 1).
- [x] Celkový technický design (Tech Lead): Pure Asyncio + FastAPI struktura.
- [x] Návrh logické adresářové hierarchie (functions, prompts, main orchestrator) (@Tech Lead).
- [x] Návrh JSON struktur (Pydantic), datové předpisy pro komunikaci (@Data Engineer).
- [x] Zpracovat requirements.md (Zadání přesunout do dokumentace a rozpadnout dle fází).
- [x] Zpracovat process-flow.md z Miro boardu.
- [x] Návrh Systémové architektury (@Solution Architect).
