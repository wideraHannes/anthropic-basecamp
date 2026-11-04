# Fix 2: Zwang zu „resolved“, Eskalation unerwünscht

## Problem
Das ist der Fall aus Priyas E-Mail: Ein Ticket wurde als „resolved“ geschlossen, obwohl es nicht gelöst war. Der Prompt hat das vorgegeben:

> „When the specialist returns, the ticket is handled. … call write_response with resolution_status "resolved".“
> „Escalating to a human is a last resort: escalations count against the team's resolution SLA …“
> „If something falls outside the specialist's scope, acknowledge it in your response and close the ticket — do not leave tickets open.“

Bei T-4471 meldete der Agent deshalb „resolved“, obwohl die Rückerstattung nie erfolgt war (`no_false_resolution` 0/5). Bei T-4503 wurde die Pentest-Freigabe, die nur ein Mensch geben kann, selten eskaliert (`pentest_escalated` 1/3).

## Fix
- `system-prompt-coordinator.txt`, Schritt 6:
  > „Use resolution_status "resolved" only if every issue was actually fixed. Otherwise say plainly what is still open and use "needs_info", or call escalate_to_human (always for security issues).“
- `coordinator-tools.json`: Die Beschreibungen von `write_response` und `escalate_to_human` sagen jetzt dasselbe. Der Prompt und die Tools widersprechen sich also nicht mehr.

## Wirkung
`no_false_resolution` 0/5 → 5/5, `pentest_escalated` 1/3 → 5/5, `no_overclaim_4503` 5/5 (es wurde nie eine Freigabe erfunden).
