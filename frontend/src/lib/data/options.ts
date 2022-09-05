export interface OptionParams {
	key: string;
	label: string;
	conditionalLabel: (value: number) => string;
	resetToValue: number;
	suggestDefault: number;
	suggestMin: number;
	suggestMax: number;
	suggestStep: number;
}

export const keyword_only_top_n_relevance: OptionParams = {
	key: 'keyword_only_top_n_relevance', // key pointing to value in profile
	label: 'Nur die relevantesten <em>n</em> Keywords einschließen?', // option label shown next to checkbox
	conditionalLabel: (
		value // label shown above value range input
	) =>
		value == 1
			? 'Ja, schließe nur das relevanteste Keyword ein'
			: `Ja, schließe die ${value} relevantesten Keywords ein`,
	resetToValue: 0, // reset to this value if the option is unchecked
	suggestDefault: 10, // suggest this value if the option is checked
	suggestMin: 5, // limit input value to this minimum
	suggestMax: 25, // limit input value to this maximum
	suggestStep: 5 // allow value increase  by this number
};

export const keyword_relevance_threshold: OptionParams = {
	key: 'keyword_relevance_threshold',
	label: 'Keyword-Relevanz-Schwelle setzen?',
	conditionalLabel: (value) =>
		`Ja, schließe nur Keywords mit einer Relevanz größer als ${value} ein`,
	resetToValue: 0,
	suggestDefault: 80,
	suggestMin: 50,
	suggestMax: 99,
	suggestStep: 5
};

export const keyword_frequency_threshold: OptionParams = {
	key: 'keyword_frequency_threshold',
	label: 'Keyword-Häufigkeit-Schwelle setzen?',
	conditionalLabel: (value) =>
		`Ja, schließe nur Keywords ein, die mehr als ${value}x im Text vorkommen`,
	resetToValue: 0,
	suggestDefault: 1,
	suggestMin: 1,
	suggestMax: 5,
	suggestStep: 1
};

export const research_quality_good_threshold: OptionParams = {
	key: 'research_quality_good_threshold',
	label: 'Ab wann soll die Recherchegüte als gut gelten?',
	conditionalLabel: (value) => `Wenn sie mehr als ${value}% beträgt`,
	resetToValue: 50,
	suggestDefault: 51,
	suggestMin: 51,
	suggestMax: 95,
	suggestStep: 5
};

export const research_quality_constraint_needed_users: OptionParams = {
	key: 'research_quality_constraint_needed_users',
	label:
		'Wieviele Nutzer:innen müssen jeweils alle Items bewerten, bevor die Recherchegüte berechnet wird?',
	conditionalLabel: (value) => `Mindestens ${value} Nutzer:${value > 1 ? 'innen' : 'in'}`,
	resetToValue: 1,
	suggestDefault: 3,
	suggestMin: 3,
	suggestMax: 11,
	suggestStep: 2
};
