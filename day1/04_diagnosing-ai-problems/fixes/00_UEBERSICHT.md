# Meridian Fixes: Übersicht

**Ergebnis:** RESOLVED 0/5 → **14/15** (T-4471 plus zwei Holdout-Tickets, je 5 Durchläufe), gleiches Modell (`claude-sonnet-5`).

| Lauf | Modell | Tickets | RESOLVED | Kosten/Durchlauf |
|---|---|---|---|---|
| Baseline | claude-sonnet-5 | T-4471 | 0/5 | $0.13 |
| „Liegt es am Modell?“ | claude-opus-4-8 | T-4471 | 0/5 | $0.26 |
| Holdout vor den Fixes | claude-sonnet-5 | alle 3 | 1/9 | $0.14 |
| **Nach den Fixes** | **claude-sonnet-5** | **alle 3** | **14/15** | **$0.15** |

| # | Fix | Datei(en) |
|---|---|---|
| 1 | [Ein Ticket, ein Specialist](01_ein-specialist-pro-ticket.md) | `system-prompt-coordinator.txt` |
| 2 | [Zwang zu „resolved“, Eskalation unerwünscht](02_falsches-resolved.md) | `system-prompt-coordinator.txt`, `coordinator-tools.json` |
| 3 | [Tool-Chaos beim Coordinator](03_tool-chaos-coordinator.md) | `coordinator-tools.json` |
| 4 | [Refund vs. Invoice-Adjustment unklar](04_billing-tools.md) | `subagent-billing-tools.json` |
| 5 | [Specialists melden nicht, was offen ist](05_specialist-uebergabe.md) | `system-prompt-subagent-*.txt` |
| – | [Noch offen: T-4503, 1 von 5](99_noch-offen.md) | – |

**Einschränkung:** Die Fixes wurden zusammen gemessen, nicht einzeln. Welcher Fix wie viel beiträgt, ist daher nur aus dem Trace und den Einzel-Checks abgeleitet, nicht isoliert nachgewiesen.
