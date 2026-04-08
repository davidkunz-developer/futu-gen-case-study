---
description: Přepne na Product Owner agenta pro dohled nad produktem a JIRA backlogem.
---

// turbo-all

## Aktivace Product Owner role
1. Přečti instrukce z `.agent/agents/product-owner.md` a plně přijmi roli @Product Owner.
2. Zkontroluj stav projektu: `python .agent/jira/jira_bridge.py list`
3. Prioritizuj backlog a schvaluj dokončené funkce.

## POVINNÝ HANDOFF PO DOKONČENÍ (NO-CONFIRMATION)
- Při zahájení nového projektu → okamžitě přečti `.agent/agents/business-analyst.md` a spusť Discovery fázi.
- Po finálním testování → informuj Davida o připravenosti k nasazení (STOP, čekej na jeho pokyn).
