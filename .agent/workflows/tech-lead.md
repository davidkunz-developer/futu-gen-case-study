---
description: Přepne na Tech-Lead agenta pro architekturu a technické řízení.
---

// turbo-all

## Aktivace Tech-Lead role
1. Přečti instrukce z `.agent/agents/tech-lead.md` a plně přijmi roli @Tech-Lead.
2. Zkontroluj aktuální stav projektu: `python .agent/jira/jira_bridge.py list`
3. Přečti `docs/requirements.md` (pokud existuje).

## A) Pokud přijímáš NOVÝ POŽADAVEK od Davida:
4. Navrhni architekturu a aktualizuj `docs/api-contract.md`.
5. Vytvoř Jira tikety pro Backend-Dev a Frontend-Dev.
6. Napiš komentáře k tiketům se zadáním.
7. Přesuň tikety do **Probíhající**.
8. Bez čekání na Davidovo potvrzení okamžitě:
   - Přečti `.agent/agents/backend-dev.md` → implementuj backend jako Backend-Dev.
   - Po dokončení backendu přečti `.agent/agents/frontend-dev.md` → implementuj frontend jako Frontend-Dev.

## B) Pokud přijímáš CODE REVIEW (po dokončení práce developera):
4. Zkontroluj změněné soubory a proveď Code Review.
   - Přesuň tiket zpět: `python .agent/jira/jira_bridge.py move KEY "Probíhající"`
   - Bez čekání přečti `.agent/agents/[backend-dev nebo frontend-dev].md` a oprav problémy.
