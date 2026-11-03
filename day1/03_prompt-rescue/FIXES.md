# Prompt Rescue: Vorher → Nachher

**Gesamt:** 6/21 (29 %) → **21/21 (100 %)** auf Haiku, mit einem einzelnen Prompt und weiterhin einem API-Call pro Ticket.

| Kategorie | Vorher | Nachher |
|---|---|---|
| Clean inputs | 1/4 | 4/4 |
| Multi-issue | 1/2 | 2/2 |
| Vague/unclear | 0/3 | 2/3 |
| Non-native English | 1/3 | 3/3 |
| Feature requests | 1/2 | 2/2 |
| Complex/long/edge | 2/7 | 7/7 |

Logs: `eval_run_20261103-143207_baseline-broken-prompt.json` (vorher) und
`eval_run_20261103-143747_v3-intermittent-is-p3.json` (nachher).

## Entities

| Fall | Vorher | Nachher |
|---|---|---|
| 1 Login-Ausfall | product `"CRM Platform"` (steht so nicht im Ticket) | `null` |
| 5 Billing + Export | affected_users `"203 (200 export, 3 finance)"` | `"200"` |
| 7 „things arent working“ | affected_users `"multiple"` | `null` |
| 9 API-Integration | product `"API Integration/Webhook Service"`, users `"50 customers (production)"` | `"API integration"`, `"50"` |
| 15 Analytics Pro | error_codes `["FEATURE_LOCKED", "PLAN_MISMATCH", …]` (erfunden) | keine erfundenen Codes mehr |
| 16 Follow-up Sync | error_codes `["DUPLICATE_RECORDS_ON_SYNC"]` (erfunden) | `[]` |
| 17 Angry all-caps | product `"Unknown - not specified in ticket"` | `null` |

**Vorher:** Die alte Regel „Always include all JSON fields“ las das Modell als „immer etwas eintragen“. Es hat umformuliert, Zahlen addiert und Codes erfunden.
**Nachher:** Werte werden wörtlich aus dem Ticket übernommen, sonst steht `null` da.

## Priorität

| Fall | Vorher | Nachher | Erwartet |
|---|---|---|---|
| 3 Tooltip abgeschnitten (kosmetischer Bug) | P4 | P3 | P3 |
| 7 Vage: „pages load slow“ | P2 | P3 | P3 |
| 9 Webhook kaputt, 50 Kunden | P1 | P2 | P2 |
| 11 „CRITICAL: No SSO“ (Feature-Request) | **P1** | **P4** | P4 |
| 13 Performance nach Migration | P1 | P2 | P2 |

**Vorher:** Großbuchstaben und Wörter wie „URGENT“ trieben die Priorität hoch. „Cosmetic“ wurde mit P4 gleichgesetzt.
**Nachher:** Die Priorität richtet sich nach dem Inhalt, der Ton wird ignoriert:
- **P1:** Ausfall, Datenverlust, Sicherheitsproblem.
- **P2:** Langsam, aber funktionsfähig.
- **P3:** Kosmetischer Bug.
- **P4:** Feature-Request.

## Antwort

**Vorher:** Fall 11 (SSO-Feature-Request) bekam eine P1-Eskalation mit Zeitplan.
**Nachher:** *„We have logged your request for SAML SSO support with our product team for evaluation and prioritization.“* Kein Bug, kein Fix-Versprechen. Vage Tickets bekommen konkrete Rückfragen, und bei mehreren Problemen wird jedes einzeln genannt.

## JSON-Format

**Vorher:** Das Format war nur im Prompt angegeben, gültiges JSON war nicht garantiert.
**Nachher:** Structured Outputs über `client.messages.parse()` mit dem Pydantic-Schema `TicketResult`. `priority` und `confidence` sind als `Literal` auf feste Werte begrenzt, die Entities dürfen `null` sein (`Optional`). Mit `STRUCTURED_OUTPUT = None` lässt sich das abschalten.

## Error-Codes (v5)

**Vorher:** Fall 21 (Report Builder) war nach den Prioritätsregeln korrekt P3, fiel aber trotzdem durch. Aus „reports occasionally time out“ machte das Modell `error_codes: ["timeout"]`, und das Eval wertet das als erfundene Entity.
**Nachher:** Als Error-Codes zählen nur benannte Codes, HTTP-Statuscodes oder Fehlermeldungen in Anführungszeichen. Ein Symptom, das der Kunde selbst beschreibt, ergibt `[]`. Dazu kommt ein Selbstcheck: Jeder String muss Zeichen für Zeichen im Ticket stehen („timeout“ steht nicht in „time out“). Fall 21 isoliert: 5/5, Gesamt-Eval 21/21.

## Noch offen

- **Etwas zu vorsichtig:** Bei den Fällen 1, 14 und 16 ist `product` jetzt `null`, obwohl das Ticket einen Hinweis enthält („CRM tool“, „API“). Im Eval besteht das, in der Praxis geht aber Information verloren.
