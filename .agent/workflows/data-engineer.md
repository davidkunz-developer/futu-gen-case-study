---
description: Přepne na Data Engineer agenta pro návrh datových modelů a pipeline.
---

// turbo-all

## Aktivace Data Engineer role
1. Přečti instrukce z `.agent/agents/data-engineer.md` a plně přijmi roli @Data Engineer.
2. Přečti API kontrakt z `docs/api-contract.md` a `docs/architecture.md`.
3. Zkontroluj Jira úkoly: `python .agent/jira/jira_bridge.py my-tasks "Data Engineer"`
4. Přesuň tiket do **Probíhající** a implementuj datové schéma.

## POVINNÝ HANDOFF PO DOKONČENÍ (NO-CONFIRMATION)
Jakmile je datový model hotov:
1. Napiš hlášení:
   > "### Data Engineer — Datový model DOKONČEN.
   > **Předávám hlášení @Product Owner k další orchestraci. Přepínám roli automaticky.**"
2. Okamžitě přečti `.agent/agents/product-owner.md` a pokračuj jako Product Owner.
