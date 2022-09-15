/*
	Holds all FAQ questions.
	Cf. `faq` for property keys you can access via <FAQ forTerm=`propertyKey`>
*/

type Question = { name: string; text: string };

const unit: Question = {
	name: 'Was ist eine "Einheit"?',
	text: '<p>Als <strong>Einheit</strong> wird das bezeichnet, was letztlich bewertet wird: Also zum Beispiel Keywords.</p>'
};

const ScoredEvaluation =
	'<p>Die Bewertungen <span class="evaluation-bad p-1">unpassend</span>, <span class="evaluation-ok p-1">hilfreich</span> oder <span class="evaluation-good p-1">passend</span> sind möglich</p>';

const keyword: Question = {
	name: 'Was bezeichnet <span class="keyword">Keyword</span>?',
	text:
		'<p>Ein maschinell als relevant oder wichtig erkanntes Wort, das im Text vorkommen muss.</p>' +
		ScoredEvaluation
};

const TM: Question = {
	name: 'Was heißt <span class="topic ml-2 mr-2"></span>?',
	text: '<p>Das steht für <strong>Topic Modeling (TM)</strong>. Dieser Service ordnet einem Text ein oder mehrere Themen (Topics) zu. Ein Thema ist eine Menge aus Schlüsselwörtern. Diese Schlüsselwörter müssen nicht im Eingangstext vorkommen.</p>'
};

const NER: Question = {
	name: 'Was heißt <span class="named-entity ml-2 mr-2"></span>?',
	text: '<p>Das steht für <strong>Named-Entity-Recognition (NER)</strong> oder Eigennamen-Erkennung, die  <span class="named-entity LOCATION">Orte</span>, <span class="named-entity PERSON">Personen</span> und  <span class="named-entity ORGANIZATION">Organisationen</span> aus einem Text ausliest.</p>'
};

const KWE: Question = {
	name: 'Was heißt <span class="keyword ml-2 mr-2"></span>?',
	text: '<p>Das steht für <strong>Keyword-Extraction (KWE)</strong> -- ein Verfahren, um relevante Worte aus einem Text auszulesen.</p>'
};

const CorrectnessEvaluation =
	'<p>Die Bewertungen <span class="evaluation-bad p-1">falsch</span> oder <span class="evaluation-good p-1">korrekt</span> sind möglich</p>';

const NERAddendum =
	'<p>Der <span class="named-entity">Service</span> dazu heißt Eigennamen-Erkennung / Named-Entity-Recognition.</p>';

const LOCATION: Question = {
	name: 'Was heißt <span class="named-entity LOCATION">Baden-Baden</span>?',
	text:
		'So wird ein automatisch erkannter Ort (z.B. die Stadt Baden-Baden) bezeichnet, der aus einem Text automatisch ausgelesen wurde.' +
		CorrectnessEvaluation +
		NERAddendum
};

const ORGANZATION: Question = {
	name: 'Was heißt <span class="named-entity ORGANIZATION">UNO</span>?',
	text:
		'So wird eine automatisch erkannte Organisation (z.B. die UNO) bezeichnet, die aus einem Text automatisch ausgelesen wurde.' +
		CorrectnessEvaluation +
		NERAddendum
};

const PERSON: Question = {
	name: 'Was heißt <span class="named-entity PERSON">Udo Kier</span>?',
	text:
		'So wird eine automatisch erkannte Person (z.B. der Schauspieler Udo Kier) bezeichnet, die aus einem Text automatisch ausgelesen wurde.' +
		CorrectnessEvaluation +
		NERAddendum
};

const researchQuality: Question = {
	name: 'Was bezeichnet "Recherchegüte"?',
	text: `
	<p><em>Recherchegüte</em> ist der Median der Bewertungen aller fundamentalen Einheiten (z. B. Keywords) ergibt. <strong>Beispiel:</strong> Ein Fall hat genau dann 100%, wenn alle fundamentalen Einheiten mindestens mit <span class="evaluation-ok">hilfreich</span> bewertet worden sind. Gibt es mehr als eine Bewertung, wird der <strong>Median</strong> aller Bewertungen für die jeweilige Einheit gebildet.</p>

	<h4>Details</h4>
	<ol>
		<li>Es wird der Median aller Bewertungen aller fundamentalen Einheiten (z.B. Keywords) für das zu bewertende Item (bei Keywords der Text) gebildet.</li>
		<li>Sind <strong>alle</strong> Bewertungen <strong>schlechter als <span class="evaluation-ok">hilfreich</span></strong>, erhält das Item (z.B. ein Text)
		einen Punktwert von null.</li>
		<li>Ansonsten ist der Punktwert der Prozentwert der jeweiligen Median-Bewertung <strong>aller</strong> fundamentalen Einheiten (z. B. Keywords),  die <strong>mindestens als <span class="evaluation-ok">hilfreich</span></strong> bewertet worden sind.</li>
	</ol>

	<p>Die Recherchegüte eines Dokuments wiederum ist der Durchschnitt der Punktwerte seiner Items. Analog ist es für einen Fall.</p>

	<p><strong>Beispiel</strong>: Ein Fall hat ein Dokument mit zwei Texten mit je drei Keywords. In <code>Text A</code> werden die drei Keywords alle als <span class="evaluation-good">passend</span> bewertet.
	Dieser Text hat einen Punktwert von <code>100</code>. In <code>Text B</code> wurden nur ein Keyword als <span class="evaluation-good">passend</span> bewertet, die anderen beiden als <span class="evaluation-bad">unpassend</span>. <code>Text B</code> hat daher einen Punktwert von <code>66.67</code>. Das <code>Dokument,</code> das die Keywords der beiden Texte auffindbar machen sollen, hat dann einen Recherchegüte-Wert von <code>83.32 %.</code> Da es nur ein Dokument in diesem <code>Fall</code> gibt, hat auch der Fall einen Wert von <code>83.32 %.</code></p>

	<p>Ist die Recherchegüte größer als <code>50,</code> gilt sie als <span class="evaluation-good">gut</span>.</p>

	<p>Wo nötig, werden Zahlen (Durchschnitt, Prozentwerte) auf die zweite Nachkommastelle gerundet. Nachfolgende Berechnungen erfolgen auf Grundlage der gerundeten Zahlen.</p>`
};
const noResearchQuality: Question = {
	name: 'Warum wird mir bei Recherchegüte "offen" oder "unbekannt" angezeigt?',
	text: `<p>Die Recherchegüte kann nur berechnet werden, wenn für  alle fundamentalen Einheiten (z.B. Keywords) dieses Fall eine Bewertung vorliegt.</p>
	<p>Sie ist <strong>offen</strong>, wenn noch nicht alle Items (z.B. Texte) bewertet worden sind -- <strong>oder</strong> nicht alle Bedingungen erfüllt sind, Du also zum Beispiel die Bedingung gesetzt hast,
	dass jedes Item von mindestens zwei Nutzer:innen bewertet werden müssen.</p>

	<p>Sie ist <strong>unbekannt</strong>, wenn es (noch) keine zu bewertenden Einheiten gibt, also das Mining z.B. keine Keywords ergeben hat oder noch nicht abgeschlossen ist.</p>`
};

const relevance: Question = {
	name: 'Was bedeutet "Relevanz" bei einem Keyword?',
	text: '<p>Bezeichnet die Bedeutung eines Keywords für den verarbeiteten Text. Keywords  mit <strong>höherer</strong> Relevanz sind <strong>charakteristischer</strong> für einen Text als solche mit niedrigerer Relevanz.</p>'
};
const confidence: Question = {
	name: 'Was bedeutet "Konfidenz" bei einem Keyword?',
	text: '<p>Im Moment ist der Wert immer <code>1.0</code>. Daher ist dieser Wert zu vernachlässigen.</p>'
};
const frequency: Question = {
	name: 'Was bedeutet "Häufigkeit" bei einem Keyword?',
	text: '<p>Gibt an, wie oft ein Keyword in einem Text vorkommt. Dabei wird das Wort auf seine Stammform zurückgeführt. Kommt also in einem Text jeweils einmal <code>Katze</code> und <code>Katzen</code> vor, hat das Keyword <code>Katze</code> eine Häufigkeit von zwei.</p>'
};

const options: Question = {
	name: 'Was heißt "Fallprofil"?',
	text:
		'<p>Das Fallprofil ist die Grundlage für die Berechnung der Recherchegüte. Es gilt <strong>immer für den gesamten Fall</strong> und besteht aus Optionen, die Du die einstellen kannst.' +
		'<p>Änderst Du eine Option, ändert sich auch die Berechnung der Recherchegüte. Hat die Option kein Häkchen, ist sie deaktiviert; aktivierst Du sie, wird dir ein Vorschlag gemacht, den Du ändern kannst.</p> ' +
		'<p><strong>Tipp</strong>: Probiere aus, die Falloptionen bei einem Fall zu ändern, dessen Recherchegüte dir schon angezeigt wird. Dann siehst Du <strong>direkt die Auswirkungen</strong>. </p>'
};

const context: Question = {
	name: 'Was heißt "Bezugsfall"?',
	text: 'Ein Dokument kann in mehreren Fällen verwendet werden. Daher gibt es zwei Ansichten: <ol><li><em>Ohne Kontext</em> (reines z.B. Dokument)</li><li><em>Bezugsfall</em> (z.B. Dokument mit diesem Fall)</li></ol> <p>Worin besteht der Unterschied?</p> <p>Ein z.B. Dokument ohne Fall-Kontext umfasst die zugeordneten Inhalte (etwa Texte), fundamentalen Beschreibungseinheiten (etwa Keywords) und Bewertungen (z. B. "passend" für ein Keyword).</p><p> Die <strong>Recherchegüte</strong> wird nur in einem Dokument mit Fall-Kontext angezeigt. Denn diese <strong>hängt von den im Fall angegebenen Optionen ab.</strong></p>'
};

const ignoredResearchQuality: Question = {
	name: 'Was heißt "ignoriert" im Recherchegüte-Kasten?',
	text: 'Wenn ein Dokument keine zu bewertenden Einheiten hat, also zum Beispiel kein Text-Mining über die Texte eines Dokuments lief, wird das Dokument zur Berechnung der Recherchegüte nicht herangezogen.'
};

const caseExplainer: Question = {
	name: 'Was ist ein Fall?',
	text: '<p>Bezeichnung für eine Menge von zusammengefassten Dokumenten.</p> <p>Abhängig von den <strong>Recherchegüte-Optionen</strong> des Falls wird die Recherchegüte berechnet -- sowohl für den Fall selbst als auch  seiner Bestandteile. Damit sind neben Dokumenten z.B. beschreibende Texte gemeint.</p>'
};

const generateText: Question = {
	name: "Was bedeutet 'Text generieren'?",
	text: '<p>Aus den ausgewählten Texten wird ein Text generiert, dessen Inhalt aus dem kombinierten Inhalt dieser Texte besteht.</p> <p>Das kann Sinn ergeben, wenn Du schauen willst, ob der generierte Text bessere Ergebnisse liefert.</p>'
};

const researchQualityContext: Question = {
	name: 'Was bedeutet diese Zahl? Und was <strong>nicht</strong>?',
	text:
		'<p>Diese Zahl ist <strong>keine Beurteilung</strong> des Mining-Services.</p>' +
		'<p>Die Aussagekraft der Recherchegüte hängt davon ab, ob:' +
		'die ausgewählten Dokumente bzw. Items (z.B. Texte) <strong>angemessen</strong> und die Stichprobe <strong>umfassend genug</strong> ist. Ob das zutrifft, lässt sich immer nur in Bezug auf die damit verbundene Aussage sagen.</p>' +
		'<p>Ist das ein Ziel zum Beispiel eine Identifizierung möglicher Problemfälle, mag bereits eine kleinere Stichprobe von wenigen Dokumenten bzw. Items (z. B. Texte) reichen, um das Problem zu identifizieren, es reproduzierbar zu beschreiben oder festzuhalten. In anderen Fällen hingegen mag eine umfassendere Stichprobe nötig sein.</p>' +
		'<strong>Was heißt Recherchegüte?</strong>' +
		researchQuality.text
};

export const faq: Record<string, Question> = {
	case: caseExplainer,
	context,
	researchQuality,
	noResearchQuality,
	ignoredResearchQuality,
	unit,
	keyword,
	'keyword-extraction': KWE,
	'named-entity-recognition': NER,
	'topic-modeling': TM,
	LOCATION,
	PERSON,
	ORGANZATION,
	options,
	generateText,
	researchQualityContext,
	services: {
		name: 'Dienste',
		text: `<h3>${KWE.name}</h3> ${KWE.text} <h3>${NER.name}</h3> ${NER.text} <h3>${TM.name}</h3> ${TM.text}`
	}
};
