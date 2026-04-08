# Business Analyst Context - FutuGen Case Study

## Analýza Odpovědí od Davida
- **Jazyk & Platforma:** Python (asyncio).
- **Audio Vstup:** Testovat na mock datech (soubor/generátor), finálně implementovat vstup z reálného mikrofonu.
- **Transkripce:** Bude striktně lokální (`openai-whisper`) pro eliminaci nákladů za API. Bude zahrnuta i speaker diarizace (pyannote.audio - splnění bonusu).
- **Klasifikace:** Použijeme Gemini API (David má k dispozici, plníme doporučený přístup 1 s LLM), pro eliminaci placené OpenAI, nebo alternativně připravíme i lokální dummy fallback. Přidáme inkrementální aktualizaci po každém chunku.
- **Bonusy:** Budou splněny všechny bonusové úlohy (WS Real-time WebSocket streaming, Docker Compose, Inkrementální klasifikace, Evaluační dataset, Speaker Diarization).
- **Visual Process:** Mám za úkol s Davidem navrhnout flow (diagram/Miro). Vytvářím první iteraci do `docs/process-flow.md`.

## Stav Subagenta
- Vytvářím `requirements.md` a `process-flow.md` (první draft).
- Čekám na validaci flow od Davida, abych mohl uzavřít svoji roli a předat to PO.
