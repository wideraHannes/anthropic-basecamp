# Fix 3: Tool-Chaos beim Coordinator

## Problem
Der Coordinator hatte 17 Tools, davon fünf für dieselbe Aufgabe (Kundendaten holen: `get_customer`, `fetch_customer_details`, `fetch_customer_v2_databricks`, `lookup_customer_info`, `customer_data_retrieval`). Dazu kamen nichtssagende Tools wie `helper`, `process`, `get_data`, `validate` und `tool_3_v2` („Updated version of tool_3“, obwohl es kein `tool_3` gibt). Die meisten Beschreibungen bestanden aus drei Wörtern („Gets a ticket“, „Writes the response.“).

Folgen: Das Modell muss bei jedem Schritt raten, welches Tool gemeint ist, verbraucht Turns und Tokens mit Fehlgriffen und bekommt keinen Hinweis, wann `resolved` gerechtfertigt ist.

## Fix
`coordinator-tools.json`: Es bleiben sieben Tools mit klarer Aufgabe: `get_ticket`, `lookup_customer_info`, `fetch_customer_details`, `check_system_status`, `spawn_specialist`, `write_response`, `escalate_to_human`. Jede Beschreibung sagt, **wofür** und **wann** das Tool eingesetzt wird, zum Beispiel:

> spawn_specialist: „… Call once per category the ticket touches.“

## Wirkung
Nicht einzeln gemessen. Erwartet sind weniger Fehlgriffe bei der Tool-Wahl, belegt ist das aber nicht. Belegt ist: Die Kosten pro Durchlauf bleiben trotz zusätzlichem Specialist bei $0.15 (Baseline $0.13).
