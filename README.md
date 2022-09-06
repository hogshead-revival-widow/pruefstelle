Tool (Prototyp) zum Qualitätsmanagement automatischer Erschließung (Textmining) im Archiv, das auf Basis menschlicher Bewertungen unter Verwendung eines festzulegenden Fallprofils einen Prozentwert ("Recherchegüte") berechnet.  

**Achtung**: Prüfstelle ist eine Alpha-Version.


# Screenshots

| | | |
|:-------------------------:|:-------------------------:|:-------------------------:|
|![Fallansicht](/screenshots/Falllansicht.png?raw=true)  Fall ansehen | ![Falloptionen](/screenshots/Falloptionen.png?raw=true) Recherchegüte wird abhängig vom Fallprofil berechnet | ![Visualisierung](/screenshots/Visualisierung.png?raw=true "Protokoll: Visualisierung") Visualisierung der Verteilung aller Bewertungen über einen Fall |
|![Hilfstexte](/screenshots/Hilfstexte.png?raw=true) Es wird möglichst wenig vorausgesetzt. Wo etwas vielleicht mal nicht klar ist, gibt's Hilfstexte. |  ![API](/screenshots/API.png?raw=true) Durchgängig modellierte/spezifizierte API (OpenAPI 3)  |![Eingabemaske](/screenshots/Eingabemaske.png?raw=true "Eingabemaske") Neuen Fall anlegen | |


# Installation 

**Vorab**: Repo klonen oder herunterladen

## Frontend

1. `cd` ins Repo
2. `cd pruefstelle/frontend/`
3. Dort `.env`-Datei nach dem Beispiel in `pruefstelle/examples` anlegen
4. `npm i`
5. `npm run dev`

*Pruefstelle* ist zwar unter http://localhost:3000/ erreichbar, wird aber einen Fehler anzeigen. Schließlich läuft das Backend noch nicht.

## Backend

1. `cd` ins Repo
2. `cd pruefstelle/backend/settings`
3. Dort `.secrets.toml` nach dem Beispiel in `pruefstelle/examples` anlegen und ggf. `config.toml` anpassen
4. `cd pruefstelle/backend`
5. `python3 -m venv .venv` 
6. `source .venv/bin/activate`
7. `pip install .`
9. `pruefstelle run` (vgl. `pruefstelle --help` für Konfigurationsmöglichkeiten)

Die API ist unter http://localhost:8000 (Swagger UI unter: http://localhost:8000/docs) erreichbar. 

Und *pruefstelle* wartet nun ohne Fehler unter http://localhost:3000. 


# Produktion

## Frontend

Statt `npm run dev` (Schritt 6) `npm run build` ausführen.  In `pruefstelle/frontend/build` finden sich nun Javascript-Dateien, die so von beliebigen Webservern statisch ausgeliefert werden können. Mehr Informationen dazu finden sich [hier](https://kit.svelte.dev/docs/adapters#supported-environments-static-sites).

Mit `npm run preview` lässt sich die Produktivbuild ausprobieren. 

## Backend

Statt `pruefstelle` (Schritt 8) `ENV_FOR_PRUEFSTELLE=production pruefstelle run` ausführen und die mit `?` markierten Werte in `pruefstelle/backend/settings/config.toml` ersetzen.

Je nach Verwendungszweck empfiehlt sich in `.secrets.toml` unter `[production.db]` eine andere Datenbank als SQLite (z. B. PostgreSQL) einzusetzen sowie uvicorn in Verbindung mit z. B. guvicorn zu nutzen; Informationen zu Letzterem finden sich [hier](https://fastapi.tiangolo.com/deployment/server-workers/).


# Nutzung

# Rollen

* **User:in**: Kann auf alle Endpunkte außer die unter [admin/] (http://localhost:8000/docs#/Administration) zugreifen
* **Superuser:in**: Kann zusätzlich auf die Endpunkte unter [admin/] (http://localhost:8000/docs#/Administration) zugreifen

# Nutzer:innen-Verwaltung

## Nutzer:in als Superuser:in anlegen

Das ist nur über die Kommandozeile möglich, siehe dazu `pruefstelle create-user --help`.

## Normale Nutzer:innen anlegen/ändern

Normale Nutzer:innenaccounts lassen sich über die [`admin/user`-Endpunkte](http://localhost:8000/docs#/Administration/create_user) anlegen/ändern.

## Kategorien

### Standardkategorien automatisch hinzufügen

Ist die [Datei `settings/fixed_categories.json` vorhanden](#weitere-einschränkungen), kann `pruefstelle populate` ausgeführt werden, um Kategorien anzulegen.

### Kategorien ändern/anlegen


Kategorien lassen sich über die [`admin/category`-Endpunkte](http://localhost:8000/docs#/Administration) anlegen/ändern


## Was ist unter welcher URL?

Wurde nichts geändert, ist *pruefstelle* nun unter http://localhost:3000 zu erreichen, die API unter http://localhost:8000 (API-Dokumentation unter: http://localhost:8000/docs).

## API-Client für Frontend automatisch generieren
 
Werden Anpassungen am Backend vorgenommen, muss ggf. der Frontend-Client aktualisiert werden. Es ist sinnvoll, die für das Frontend irrelevanten Adminrouten vorab auszukommentieren (unter `backend/pruefstelle/routes/__init__.py`).

Dazu ist unter http://localhost:8000/openapi.json die automatisch erzeugte API-Spezifikation verfügbar. Mit dieser kann per `npx swagger-typescript-api -p openapi.json -o ./src --unwrap-response-data --single-http-client --modular` ein Client erzeugt werden.

Nun bitte die in den Dateien in  `frontend/lib/api` dokumentierten Änderungen vornehmen und die dort vorhandenen Dateien durch die generierten ersetzen.

# Einschränkungen
 
*prüfstelle* hat einen begrenzten Einsatzzweck. Ziel ist nicht die Bewertung von Verfahren zur automatischen Klassifizierung ("Künstliche Intelligenz") an sich.

Vielmehr kann mit *prüfstelle* aus der Perspektive ausgewählter Beispielfälle **exploriert** werden, unter welchen Weiterverarbeitungsbedingungen was wie gut funktioniert. Der Blick geht dabei vom Besonderen auf das Allgemeine, was eine Verallgemeinerung nur unter bestimmten Bedingungen erlaubt. Statt also zu fragen "was kann die Maschine?" ist die Frageperspektive hier: "Wie gut funktioniert das für mein Archivgut?".

Viele Hilfstexte helfen dabei, Berühungsängste mit automatischen Klassifizieren abzubauen und so mithilfe von *prüfstelle* Einsatzzwecke in einer kontrollierten Umgebung zu erproben.

 
 ## Weitere Einschränkungen
 
* Im jetzigen Zustand ist Prüfstelle nur nutzbar, wenn Zugriff auf interne Services besteht; Hinweise auf zu ersetzende Elemente bei Einsatz mit anderen Services geben die Dateien in `backend/settings/`
* `pruefstelle populate` funktioniert nur, wenn die Datei `settings/fixed_categories.json` vorhanden ist, die ich nicht mit ausliefern kann; zur dort erwarteten Struktur vgl. das dort genutzte Modell.
* Die vorhandene Authentifizierung ist dazu gedacht, mehrere Bewertungen durch verschiedene Personen zu ermöglichen und dabei möglichst komfortabel zu sein. Sie ist nicht auf Sicherheit ausgelegt. Es ist keine gute Idee, *Prüfstelle* ohne weitere Maßnahmen außerhalb eines gesicherten, internen Netzes zu betreiben.
* Die Datenbankabfragen sind nicht optimiert.



 
