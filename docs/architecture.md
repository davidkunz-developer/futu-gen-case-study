# System Architecture: FutuGen Audio Pipeline

## Technology Stack
- **Language Framework**: `Python 3.10+` with `asyncio`
- **Audio Intake Layer**: `pyaudio` (Live) / `soundfile` (Mock)
- **Transcription Layer**: `openai-whisper` (Local execution)
- **Diarization Layer**: `pyannote.audio`
- **Classification Layer**: `google-generativeai` (Gemini API for LLM)
- **Streaming/API**: `FastAPI` (for WebSocket broadcasting)
- **Containerization**: `Docker` & `Docker Compose`

---
### 🛡️ Justification for Technology Exception (Deepgram Pivot)
Dle zadání byla testována kombinace **OpenAI Whisper + Pyannote**, která však v lokálním/hybridním prostředí vykazovala latenci přesahující 2–4 sekundy. Pro projekt **FutuGen**, kde je kritickým požadavkem „Real-Time Boží“ zážitek s odezvou pod 1 vteřinu, jsme se rozhodli využít výjimku v zadání a nasadit **Deepgram Nova-2**. 

**Hlavní přínosy Deepgramu:**
1. **Sub-300ms latence** (přepis probíhá streamovaně po slovech).
2. **Integrated Speaker Diarization** (není nutné běžet druhý pomalý model, což šetří 100 % CPU režie lokálního stroje).
3. **Vyšší stabilita mluvčích S1–S4** díky kontinuálnímu poslechu jednoho modelu.
---

## Component Modules (Snake Case for Miro Mapping)

1. `audio_intake`  
   Tato služba nepřetržitě odebírá surový zvuk do paměti a seká ho na cca 2s asynchronní bloky (tzv. "chunky").

2. `processing_queue`
   Jedná se o chytrou frontu `asyncio.Queue`, která brání systému, aby se zahltil, když transkripce na chvíli trvá déle než nahrávání.

3. `transcription_engine`
   Transformuje audio chunky na text pomocí asynchronního dotazu na OpenAI Whisper API.

4. `speaker_diarization` [Bonus branch]
   Běží asynchronně podél transkripce a detekuje změnu mluvčího z audio stop v pozadí.

5. `record_compiler`
   Spojuje výstupy z transkripce a případné diarizace, formátuje je do zadaného formátu `JSONL` a přiděluje jim timestamps.

6. `llm_classifier`
   Odebírá stream čistého textu a skrze OpenAI GPT-4o-mini určuje logickým Prompt Engineeringem, zda jde o `private` (rodina/osobní hovor) nebo `topic_based` konverzaci, plus klíčová témata.

7. `event_broadcaster`
   FastAPI webový server udržující otevřený websocket. Vystřeluje každou novou transkripci a aktualizaci z klasifikátoru divákům.

## Sequence Flow
1. Audio přichází do `audio_intake`.
2. Předává se do `processing_queue`.
3. Z `processing_queue` se audio paralelně předává do `transcription_engine` (přepis textu) a do `speaker_diarization` (identifikace osoby). Obě tyto větve posílají své výsledky, které se spojí v uzlu `record_compiler`.
4. Výsledek z kompilátoru propadne paralelně do `event_broadcaster` k živému odeslání a zároveň do `llm_classifier` k provedení analytické logiky (LLM evaluace textu).
5. Klasifikátor (`llm_classifier`) nakonec vrátí svůj analytický výsledek zpět do uzlu `event_broadcaster`, aby i tento výsledek mohl být odvysílán divákovi.
