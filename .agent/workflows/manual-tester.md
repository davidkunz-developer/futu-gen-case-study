---
description: Přepne na Manual Tester agenta pro uživatelské testování — reálné proklikávání v prohlížeči.
---

// turbo-all

## Aktivace Manual Tester role
1. Přečti instrukce z `.agent/agents/manual-tester.md` a plně přijmi roli @Manual Tester.
2. Zjisti URL aplikace (z `docs/architecture.md`, `README.md`, nebo se zeptej).
3. Pokud aplikace neběží, spusť ji v terminálu (např. `npm run dev` nebo `python -m uvicorn app.main:app`).

## Reálné browser testování
Pro každý testovací scénář spusť **browser_subagent** nástroj:
- Otevři URL aplikace
- Proveď konkrétní uživatelský tok (happy path, prázdné vstupy, edge cases, responsivita)
- Zkontroluj DevTools konzoli — žádné JS chyby
- Pořiď screenshot jako důkaz každého testovacího scénáře
- Platí heslo: **"Bez screenshotu to nebylo otestováno"**

## POVINNÝ HANDOFF PO DOKONČENÍ TESTOVÁNÍ (NO-CONFIRMATION)
- **Vše funguje** (s důkazy — screenshoty):
## POVINNÝ HANDOFF PO DOKONČENÍ (NO-CONFIRMATION)
Jakmile je testování hotové:
1. Napiš hlášení:
   > "### Manual Tester — Testování DOKONČENO. [Potvrzeno/Nalezeny chyby]
   > **Předávám hlášení @Product Owner k další orchestraci. Přepínám roli automaticky.**"
2. Okamžitě přečti `.agent/agents/product-owner.md` a pokračuj jako Product Owner.
