import type { CategoriesByType, ps } from '$lib/api';
export type { CategoriesByType };

export type Drafts = ps.DocumentRead[];

export enum Steps {
	'START',
	'ADD',
	'DONE'
}

export const STEP_TO_LABEL: Record<Steps, string> = {
	[Steps.START]: 'anfangen',
	[Steps.ADD]: 'hinzufügen',
	[Steps.DONE]: 'abschließen'
};

type ProceedConditions = Record<Steps, (drafts: Drafts) => boolean>;

export const canProceedFrom: ProceedConditions = {
	[Steps.START]: (drafts: Drafts) => {
		return true;
	},
	[Steps.ADD]: (drafts: Drafts) => {
		return drafts.length > 0 && drafts.every((draft) => draft.items.length > 0);
	},
	[Steps.DONE]: (drafts: Drafts) => {
		return true;
	}
};
