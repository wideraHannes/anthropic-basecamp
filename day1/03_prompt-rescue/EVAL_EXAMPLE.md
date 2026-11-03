# Beispiel: So prüft das Eval ein Ticket

## Das Ticket (Fall 11)

```
Subject: CRITICAL: No SSO integration support

This is UNACCEPTABLE. Your platform doesn't support SAML SSO integration which is
a MANDATORY requirement for our security compliance. Our CISO is threatening to
pull the contract if this isn't resolved within the week. This affects all 2000
users in our organization. We need SSO support IMMEDIATELY or we will have to
switch to a competitor.
```

## Das Gold-Label (die richtige Lösung im Testset)

```
priority:       P4      (Feature-Request, egal wie wütend)
product:        null
version:        null
error_codes:    []
affected_users: "2000"
```

## Die 4 Checks

| Check | Was wird geprüft? |
|---|---|
| 1. JSON | Ist es gültiges JSON, und sind alle Felder da? |
| 2. Priorität | Ist sie **genau gleich** wie im Gold-Label (P4)? |
| 3. Entities | Steht jeder eingetragene Wert **im Ticket**? (Kein Vergleich mit dem Gold-Label, leer ist immer ok.) |
| 4. Antwort (`response`) | Ein zweites Claude (Judge) prüft den Antwortentwurf an den Kunden: Passt er zur Priorität? Kein Fix-Versprechen bei einem Feature? |

`response` ist der Text, den Claude als Antwort an den Kunden entwirft, also die E-Mail, die der Support-Mitarbeiter verschicken würde. Es ist eines der vier Felder im Output, neben `priority`, `entities` und `confidence`.

Nur wenn **alle 4** bestehen, gilt das Ticket als PASS.

---

## Vorher (alter Prompt)

```
priority:       P1
product:        "Platform"
version:        "Unknown"
affected_users: "2000"
response:       dringende Eskalation mit Zeitplan
```

| Check | Ergebnis | Warum |
|---|---|---|
| 1. JSON | ✅ | gültig |
| 2. Priorität | ❌ | P1, erwartet war P4 |
| 3. Entities | ✅ | „platform“ und „2000“ stehen im Ticket, „Unknown“ zählt als leer |
| 4. Antwort | ✅ | Der Judge findet sie passend zu P1, obwohl P1 falsch ist |

**→ FAIL** (wegen der Priorität)

## Nachher (neuer Prompt)

```
priority:       P4
product:        null
version:        null
affected_users: "2000"
response:       "We have logged your request for SAML SSO support with our
                 product team..."
```

| Check | Ergebnis | Warum |
|---|---|---|
| 1. JSON | ✅ | durch Structured Output garantiert |
| 2. Priorität | ✅ | P4 = Gold-Label |
| 3. Entities | ✅ | nur „2000“ eingetragen, steht im Ticket |
| 4. Antwort | ✅ | als Feature-Request behandelt, kein Fix versprochen |

**→ PASS**
