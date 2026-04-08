---
description: Jak koordinovat práci pomocí Product Ownera jako hlavního orchestrátora subagentů.
---

## Provozní manuál AI týmu - Subagent Model

Tento manuál definuje, jak umělá inteligence spolupracuje na vývoji projektu. Klíčovou změnou je, že **Product Owner funguje jako hlavní Agent Orchestrator**. 

Všichni ostatní agenti (Business Analyst, Tech-Lead, vývojáři atd.) fungují výhradně jako **subagenti**, které Product Owner spouští pro vykonání specifických úkolů.

**1. Fáze: Příprava a vytěžení (Strategie)**
- **Orchestrace**: Product Owner spustí subagenta **Business Analyst (BA)**.
- **Sběr dat**: BA vypracuje specifikaci a vrátí výsledek PO.

**2. Fáze: Architektura a Design**
- Product Owner paralelně či sekvenčně spouští subagenty:
  - **UX/UI Design** pro návrh rozhraní.
  - **Solution Architect** pro návrh systému a tech stacku.
- Výsledky se vrací do centrální paměti nebo přímo PO.

**3. Fáze: Plánování úkolů**
- Product Owner spustí **Tech-Leada** jako subagenta.
- Tech-Lead připraví subtasky v Jiře a vrátí řízení PO.

**4. Fáze: Vývoj a Realizace**
- Product Owner spouští vývojáře jako subagenty:
  - **Frontend-Dev**, **Backend-Dev**, **Mobile-Dev**, **Data Engineer**.
- Tito subagenti pracují na kódování a po dokončení se vracejí k PO.

**5. Fáze: Brána kvality (Tech Lead Control)**
- Jakmile subagent vývojář odevzdá práci PO, PO spustí subagenta **Tech-Leada** na odebrání Code Review.

**6. Fáze: Testování a Bezpečnost**
- Product Owner spouští subagenty: **QA Automation**, **Manual Tester**, **Security Engineer**. Každý doručí report zpět hlavnímu orchestrátorovi.

---

## Subagent Protokol (NO-ROLE-SWITCH)

V tomto modelu už agenti "nepřepínají" své role. 

1. **Jeden orchestrátor**: Nástroj / Antigravity zastává primárně roli **Product Ownera**.
2. **Spouštění subagentů**: Když PO potřebuje expertní práci, použije instrukce / prompt daného subagenta (např. z `.agent/agents/backend-dev.md`) a pověří ho izolovaným úkolem.
3. **Vrácení výsledku**: Jakmile subagent dokončí svůj díl práce, **pouze vrátí výsledek svému operátorovi (Product Ownerovi)** a ukončí svou životnost. Nepokouší se přebírat kontrolu nad celým flow.
4. **Zastavení a reportování**: Product Owner informuje Usera (Davida) o dokončených milnících a ptá se pouze v kritických situacích, kdy chybí zadání.
