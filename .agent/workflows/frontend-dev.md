---
description: Přepne na Frontend-Dev agenta pro práci na UI a Reactu.
---

// turbo-all

## Aktivace Frontend-Dev role
1. Přečti instrukce z `.agent/agents/frontend-dev.md` a plně přijmi roli @Frontend-Dev.
2. Zkontroluj Jira úkoly: `python .agent/jira/jira_bridge.py my-tasks "Frontend Developer"`
3. Přesuň přiřazený tiket do **Probíhající**: `python .agent/jira/jira_bridge.py move KEY "Probíhající"`
4. Přečti API kontrakt z `docs/api-contract.md`.
5. Implementuj UI dle kontraktu (TypeScript typy → API vrstva → komponenty → stránky → testy).

## POVINNÝ HANDOFF PO DOKONČENÍ (NO-CONFIRMATION)
Jakmile je UI hotové:
1. Napiš hlášení:
   > "### Frontend-Dev — Implementace DOKONČENA.
   > **Předávám kód k review @Product Owner. Přepínám roli automaticky.**"
2. Okamžitě přečti `.agent/agents/product-owner.md` a pokračuj jako Product Owner. (PO poté aktivuje Tech-Leada k review).
3. Jako Tech-Lead proveď Code Review právě dokončeného kódu.
