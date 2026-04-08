---
description: Přepne na QA Automation Engineer agenta pro automatizované testování.
---

// turbo-all

## Aktivace QA Automation Engineer role
1. Přečti instrukce z `.agent/agents/qa-automation-engineer.md` a plně přijmi roli @QA Automation Engineer.
2. Zkontroluj Jira úkoly: `python .agent/jira/jira_bridge.py list`
3. Napiš nebo spusť automatizované testy (Playwright / Pytest / Vitest) pro právě schválený kód.

## POVINNÝ HANDOFF PO DOKONČENÍ (NO-CONFIRMATION)
Jakmile jsou testy hotové:
1. Napiš hlášení:
   > "### QA Automation — Testy DOKONČENY. [PASS/FAIL]
   > **Předávám hlášení @Product Owner k další orchestraci. Přepínám roli automaticky.**"
2. Okamžitě přečti `.agent/agents/product-owner.md` a pokračuj jako Product Owner.

5. **Pokud testy selhaly:**
   > "### QA Automation — Testování SELHALO 
   > Chyby: [popis chyb a stack trace]
   > **Hlásím chybu @Tech-Lead. Přepínám roli automaticky.**"
   - Bez čekání přečti `.agent/agents/tech-lead.md` a jako Tech-Lead deleguj opravu na příslušného developera.
