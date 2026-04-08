---
description: Přepne na Backend-Dev agenta pro práci na API a FastAPI.
---

// turbo-all

## Aktivace Backend-Dev role
1. Přečti instrukce z `.agent/agents/backend-dev.md` a plně přijmi roli @Backend-Dev.
2. Zkontroluj Jira úkoly: `python .agent/jira/jira_bridge.py my-tasks "Backend Developer"`
3. Přesuň přiřazený tiket do **Probíhající**: `python .agent/jira/jira_bridge.py move KEY "Probíhající"`
4. Přečti API kontrakt z `docs/api-contract.md`.
5. Implementuj backend dle kontraktu (modely → services → routery → testy).

## POVINNÝ HANDOFF PO DOKONČENÍ (NO-CONFIRMATION)
Jakmile je kód hotový:
1. Napiš hlášení:
   > "### 💻 Backend-Dev — Implementace DOKONČENA.
   > **Předávám kód k review @Product Owner. Přepínám roli automaticky.**"
2. Okamžitě přečti `.agent/agents/product-owner.md` a pokračuj jako Product Owner. (PO poté aktivuje Tech-Leada k review).
3. Jako Tech-Lead proveď Code Review právě dokončeného kódu.
