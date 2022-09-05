Frontend des Prototypen zur Evaluierung von Mining-Services auf Basis von intellektuellen Bewertungen.

Zur Vereinfachung des Zusammenspiels zwischen Frontend und API kann unmittelbar ein Typescript/fetch-Client (vgl. unten) aus der `openapi.json` der API generiert werden.

# Installieren

`npm install`

# Konfigurieren

Es ist eine minimale Konfiguration nötig. Diese erfolgt über eine ggf. anzulegende `.env`-Datei. Die `.env`-Datei muss das folgende enthalten (Beispielwerte):

> VITE_MAIL_CONTACT_ERROR='fehler@beispiel.de
> VITE_API_DOCS_URL='http://localhost:8000/docs'
> VITE_API_BASE_URL='http://localhost:8000'
> VITE_API_UPDATE_INTERVAL=1500

`VITE_API_UPDATE_INTERVAL` erwartet einen Wert in Millisekunden und bestimmt, in welchen Zeitabständen bei der API nachgefragt wird, ob längerlaufende Tasks (heißt konkret: das Named-Entity- bzw. Keyword-Mining) abgeschlossen sind.

`VITE_MAIL_CONTACT_ERROR` wird bei Fehlermeldungen als Kontaktemailadresse angezeigt.
Die anderen beiden URLs zeigen auf die Prüfstelle-API.

Optische Einstellungen können in _tailwind.config.cjs_ vorgenommen werden. Eine beispielhafte Anpassung des Standardtemplates ist dort zu finden.

# Bündeln

## Entwicklung

Zur Entwicklung: `npm run dev` eingeben. Der lokale Entwicklungsserver ist über [http://localhost:3000](http://localhost:3000) erreichbar.

Alternativ kann über `npm run preview` auf Basis der **build/**-Dateien eine Vorschauversion gebaut werden.

## Produktion

Produktion: `npm run build`

Die gebündelten, kompilierten (wie es die Sveltedocs nennen) Vanilla-Javascript-Dateien finden sich nun in **build/**.

Das kann nun grundsätzlichen direkt so über einen beliebigen Webserver ausgeliefert werden. Ggf. sind allerdings weitere Anpassungen nötig, um falsche 404-Fehler zu vermeiden (für nginx etwa: ` try_files $uri $uri/ $uri.html /200.html;`). Die `200.html`-Fallback-Seite wird ebenfalls von `npm run build` generiert.

# Typescript/fetch-client aus openapi.json generieren

Mithilfe dieses Kommandos lässt sich eine typescript/fetch-API aus der von der Prüfstelle-API bereitgestellten `openapi.json` generieren:

> npx swagger-typescript-api -p http://localhost:8000/openapi.json -o ./src --unwrap-response-data --single-http-client --modular

Das setzt voraus, dass die API unter http://localhost:8000 erreichbar ist und ein Verzeichnis _src_ unterhalb des aktuellen Verzeichnis' existiert. Vgl. (https://github.com/acacode/swagger-typescript-api)[Swagger Typescript] für mehr Informationen zu `swagger-typescript-api`.

**Nota bene**: Es wird eine minimal angepasste Version des generierten Clients genutzt, um ihn mit Svelte kompatibel zu machen. Die Anpassungen sind in den Dateien in **src/lib/api** dokumentiert, die den gleichen Namen wie die generierten Dateien haben.

# Orientieren

## Verzeichnisstruktur

Überblick über die wichtigsten Verzeichnisse:

- **src/lib/api**: Alles, was direkt mit der Interaktion mit der API zu tun hat (vgl. oben zur Generierung des Clients)
- **src/lib/components**: Enthält die einzelnen Komponenten; in dem Unterverzeichnis **src/lib/components/basic** finden sich einfache (d.h. nicht zusammengesetzte), komplexere Komponenten sind ggf. je in weiteren Unterverzeichnissen zusammengefasst. **Nota bene**: Der Einfachheit halber sind die Bausteine für diesen Prototypen in der Regel nicht sauber gekapselt, so wird z.B. in **src/lib/components/case/Options.svelte** auch die Aktualisierung der Falloptionen direkt in der Komponente erledigt. Eine Ausnahme ist z.B. **src/lib/components/alert**; die Funktionlität, die nicht unmittelbar zur Komponente gehört, findet sich in der korrespondierenden Datei in **src/lib/scripts**, hier: **src/lib/scripts/alerts.ts**.
- **src/lib/scripts**: Enthält (vgl. oben zu **src/lib/components**) sowohl Funktionalitäten, die über die unmittelbare Komponente hinausgeht als auch Funktionen, die von mehreren Komponenten genutzt werden.
- **src/routes**: Hier finden sich alle Routen; nähere Informationen zu dynamischen Routen bzw. besonderen Dateien wie z.B. `__layout.svelte` finden sich in der (https://kit.svelte.dev/docs/routing)[Sveltekit-Dokumentation]
