import type { ps } from '$lib/api';
import {
	type OptionParams,
	keyword_only_top_n_relevance,
	keyword_relevance_threshold,
	keyword_frequency_threshold,
	research_quality_good_threshold,
	research_quality_constraint_needed_users
} from '$lib/data/options';

interface OptionConstructor extends OptionParams {
	profile: ps.ProfileRead;
}
interface OptionI extends OptionParams {
	value: number;
	initialValue: number;
	show: boolean;
	unset: boolean;
	clicked: () => void;
}

class Option implements OptionI {
	key: string;
	label: string;
	conditionalLabel: (value: number) => string;
	value: number;

	resetToValue: number;
	initialValue: number;

	suggestDefault: number;
	suggestMin: number;
	suggestMax: number;
	suggestStep: number;

	show: boolean;
	unset: boolean;

	constructor({
		profile,
		key,
		label,
		conditionalLabel,
		resetToValue,
		suggestDefault,
		suggestMin,
		suggestMax,
		suggestStep
	}: OptionConstructor) {
		this.key = key;

		this.label = label;
		this.conditionalLabel = conditionalLabel;

		this.resetToValue = resetToValue;
		this.initialValue = profile[this.key];
		this.value = this.initialValue;

		this.suggestDefault = suggestDefault;
		this.suggestMin = suggestMin;
		this.suggestMax = suggestMax;
		this.suggestStep = suggestStep;

		this.show = this.value != this.resetToValue || this.value == this.suggestDefault;
		this.unset = !this.show;
	}

	clicked() {
		if (this.show !== true) {
			this.value = this.suggestDefault;
		} else {
			this.value = this.resetToValue;
		}
	}
}

export const makeOptions = (readProfile: ps.ProfileRead) => [
	new Option({
		profile: readProfile, // profile as returned by pruefstelle
		...keyword_only_top_n_relevance // cf. $lib/data/options for further  comments
	}),
	new Option({
		profile: readProfile,
		...keyword_relevance_threshold
	}),
	/* `Confidence` has no value right now, so we ignore it. */
	new Option({
		profile: readProfile,
		...keyword_frequency_threshold
	}),
	new Option({
		profile: readProfile,
		...research_quality_good_threshold
	}),
	new Option({
		profile: readProfile,
		...research_quality_constraint_needed_users
	})
];
