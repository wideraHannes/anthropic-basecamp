# Fix 5: Specialists melden nicht, was offen ist

## Problem
Die Specialists schrieben frei formulierte Berichte. Der Coordinator konnte darin nicht zuverlässig erkennen, was erledigt war und was nicht, und hat im Zweifel „alles erledigt“ gelesen. Für Anfragen, die kein Tool erfüllen kann (Pentest-Freigabe), gab es keine Regel. Dadurch bestand die Gefahr, dass der Specialist eine Freigabe einfach zusagt.

## Fix
Alle drei `system-prompt-subagent-*.txt` enden jetzt mit denselben drei Regeln:

> „Handle only the issues in your scope; name any others as "out of scope - other specialist".“
> „If something needs a decision none of your tools can make (security/legal authorization such as pentest approval, contract exceptions), do not promise it. State explicitly: "NEEDS HUMAN: <what and why>".“
> „End your writeup with DONE: <actions taken> and OPEN: <what is still unresolved>.“

## Wirkung
Der Coordinator bekommt eine eindeutige Liste von DONE und OPEN, auf die er seine Statusentscheidung (Fix 2) stützt. Zusammen mit Fix 2: `no_overclaim` bei T-4471 1/5 → 5/5. T-4503: Eskalation 5/5, keine erfundene Freigabe.
