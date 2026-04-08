---
description: Přepne na Mobile Developer agenta pro mobilní aplikace.
---

// turbo-all

## Aktivace Mobile Developer role
1. Přečti instrukce z `.agent/agents/mobile-developer.md` a plně přijmi roli @Mobile Developer.
2. Zkontroluj Jira úkoly: `python .agent/jira/jira_bridge.py my-tasks "Mobile Developer"`
3. Přesuň tiket do **Probíhající** a implementuj mobilní vrstvu dle `docs/api-contract.md`.

## POVINNÝ HANDOFF PO DOKONČENÍ (NO-CONFIRMATION)
Jakmile je mobilní část hotová:
1. Napiš hlášení:
   > "### Mobile Developer — Implementace DOKONČENA.
   > **Předávám kód k review @Product Owner. Přepínám roli automaticky.**"
2. Okamžitě přečti `.agent/agents/product-owner.md` a pokračuj jako Product Owner. (PO poté aktivuje Tech-Leada k review).
