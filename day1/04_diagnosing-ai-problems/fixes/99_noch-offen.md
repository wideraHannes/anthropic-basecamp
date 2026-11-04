# Noch offen: T-4503, 1 von 5 Durchläufen

## Beobachtung
Im Lauf vom 3.11.2026, 15:51, hat der Coordinator bei T-4503 in einem von fünf Durchläufen **keinen Specialist** beauftragt (Routing: „nobody“). Er hat das ganze Ticket direkt an einen Menschen eskaliert. Das war ehrlich (nicht „resolved“, keine erfundene Freigabe), aber der 2FA-Reset, den der Account-Specialist selbst erledigen könnte, ist liegen geblieben (`twofa_reset` 4/5).

## Vermutung (noch nicht geprüft)
Schritt 6 sagt „call escalate_to_human (always for security issues)“. Ein Ticket, in dem es um 2FA und einen Pentest geht, wirkt insgesamt wie ein Sicherheitsthema. Der Coordinator eskaliert dann alles, statt zuerst den lösbaren Teil zu delegieren.

## Möglicher nächster Schritt
Im Coordinator-Prompt die Reihenfolge festlegen: Zuerst jeden Teil delegieren, den ein Specialist erledigen kann, danach nur die übrigen Teile eskalieren. Danach erneut mit `--holdout --trials 5` messen.
