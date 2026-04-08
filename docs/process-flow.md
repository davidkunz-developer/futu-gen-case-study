# Procesní Flow Architektury

Tento dokument představuje vizualizaci asynchronního pipelinu od vstupu audio dat až po real-time zobrazování na straně testovacího klienta.

```mermaid
flowchart TD
    %% Zdroje Dat
    subgraph Input [Modul 1: Audio Streaming]
        M(Reálný Mikrofon) --> |raw bytes| N[Audio Normalizer & Chunker]
        F(Mock WAV Soubor) --> |chunking| N
        N --> |Chunk (1-3s, 16kHz, overlap)| AQ((Audio Async Queue))
    end

    %% Transkripce a Analýza audia
    subgraph Whisper_Module [Modul 2: Transcription Engine]
        AQ --> |Vyčítání popředí| W{Local Whisper Inference}
        W --> |Sliding context window| W
        AQ --> |Analýza pozadí| D[Pyannote Diarization]
        W --> |Text segmentu| TM(Text Merger / JSONL Builder)
        D --> |Identifikace mluvčího| TM
        TM --> |Event: New Transcript| J1[(Záznam .jsonl)]
    end

    %% Klasifikace textu
    subgraph Classifier_Module [Modul 3: LLM Classifier]
        J1 --> |Čtení posledních N záznamů| LLM[OpenAI API (gpt-4o-mini) / Sliding Window Prompt]
        LLM --> |Inkrementální posouzení| OUT_C{Klasifikace JSON}
        OUT_C --> |Topic-based / Private| EventBus((Event / Broadcast Bus))
    end

    %% Výstup
    subgraph Output_Module [Příjemci Výstupů]
        TM --> |Event: Transcript| EventBus
        EventBus --> |WebSocket Push| WS_Client(Live Dashboard Klient)
        EventBus --> |Log files| Final_Logs[(Výsledný Classifier Log)]
    end
```

### Specifika procesu
1. Systém je striktně asynchronní. `Audio Async Queue` zabraňuje tomu, aby pomalejší zpracování Whisperu zaseklo nahrávání audia (tzv. blocking I/O).
2. Diarizace běží nezávisle a obohacuje metadata o novém mluvčím zpětně, jakmile si je jistá.
3. Obnovený "Event Bus" odesílá data jak do WebSockets (FastAPI websocket endpoint), tak spouští inkrementální re-klasifikaci u OpenAI API s novým kontextem.
