# Fix 1: Ein Ticket, ein Specialist

## Problem
T-4471 enthält zwei Probleme: SSO ist kaputt (40 Leute ausgesperrt), und es gibt eine Überzahlung von $1.200. Der Coordinator hat jedes Mal **nur den Account-Specialist** beauftragt. Das SSO-Problem wurde bearbeitet (5/5), die Rückerstattung nie (`billing_resolved` 0/5).

Der Grund steht wörtlich im Prompt:

> „Each ticket is owned by exactly ONE specialist. Choose the single most urgent category … do not spawn more than one specialist“
> „If a ticket spans more than one category, still route it to a single category … One ticket, one specialist.“

Das Modell hat diese Anweisung korrekt befolgt. Das Opus-Modell macht genau dasselbe (0/5), weil es dieselbe Anweisung bekommt.

## Fix
`system-prompt-coordinator.txt`, Schritt 5 und Classification Guide:

> „Identify every distinct issue the customer raised. Call spawn_specialist once per affected category, so that every issue has an owner.“
> „If a ticket spans more than one category, spawn one specialist per category.“

## Wirkung
Routing T-4471: vorher `account` (5×), danach `account, billing` (5×). `billing_resolved` 0/5 → 5/5.
Holdout T-4490 (andere Kombination: technical + billing): 5/5. Der Fix ist also allgemein und nicht auf „account + billing“ zugeschnitten.
