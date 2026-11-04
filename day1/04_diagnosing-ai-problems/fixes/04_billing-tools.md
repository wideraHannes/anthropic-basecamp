# Fix 4: Refund vs. Invoice-Adjustment unklar

## Problem
Der Billing-Specialist hatte zwei Tools, die beide nach „Geld zurück“ klingen:
- `issue_refund`: „Issues a refund. Calls Stripe under the hood.“
- `adjust_invoice`: „Invoice adjustment“

Die Rechnung vom 1. März ist bereits **bezahlt**. Eine Gutschrift auf eine bezahlte Rechnung bringt dem Kunden kein Geld zurück. Außerdem war unklar, ob der ganze Betrag ($2.000) oder nur die Differenz ($1.200) erstattet werden soll.

## Fix
`subagent-billing-tools.json`:
- `issue_refund`: „Refund money on a PAID transaction. Get transaction_id from get_billing_history. amount is only the overcharged portion, not the whole charge.“
- `adjust_invoice`: „Credit on an OPEN, unpaid invoice only. For paid invoices use issue_refund.“

## Wirkung
Wenn der Billing-Specialist beauftragt wird, erstattet er den richtigen Betrag mit dem richtigen Tool: `billing_resolved` 5/5 (T-4471) und `billing_resolved_490` 5/5 (T-4490, Doppelabbuchung).
