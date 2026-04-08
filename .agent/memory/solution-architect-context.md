# Solution Architect Context - FutuGen Case Study

## Aktuální úkol
- Vytvořit system design a architekturu na základě `docs/requirements.md`.
- Na žádost Davida jsem integroval `snake_case` pojmenování základních komponent (pro Miro board).

## Tech Stack
- Míříme na **Python 3.10+ (asyncio)** pro IO/blocking operace bez čekání.
- **Whisper** poběží lokálně asynchronně.
- **Gemini API** poskytne levnou/rychlou klasifikaci.

## Výstupy sítě
- Zpracováno ucelené zobrazení do `docs/architecture.md`.
