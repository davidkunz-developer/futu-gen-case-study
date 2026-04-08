---
description: Přepne na Security Engineer agenta pro audit a bezpečnost.
---

// turbo-all

## Aktivace Security Engineer role
1. Přečti instrukce z `.agent/agents/security-engineer.md` a plně přijmi roli @Security Engineer.
2. Proveď security audit kódu (auth, data protection, API security, zranitelnosti).

## POVINNÝ HANDOFF PO DOKONČENÍ (NO-CONFIRMATION)
Jakmile je audit hotov:
1. Napiš hlášení:
   > "### Security Engineer — Audit DOKONČEN. [Bezpečné/Nalezeny rizikové body]
   > **Předávám hlášení @Product Owner k finálnímu releasu. Přepínám roli automaticky.**"
2. Okamžitě přečti `.agent/agents/product-owner.md` a pokračuj jako Product Owner. informuj Davida.

- **Nalezeny problémy:**
  1. Napiš: > "### Security Engineer — Security Audit SELHAL . Zranitelnosti: [seznam]. **Hlásím @Tech-Lead. Přepínám roli automaticky.**"
  2. Bez čekání přečti `.agent/agents/tech-lead.md` a deleguj opravy.
