import { get as $ } from 'svelte/store';

import { user } from '$lib/stores';

import { ps, ResultType, isKeyword, EvaluationType } from '$lib/api';
import { getShortIfNeeded } from '$lib/utils';
import { NAMED_ENTITY_TO_WORD_WITH_ARTICLE } from '$lib/data/namedEntities';

export type TitleData = { item_id: string; title: string; document_id: string };

export class EvaluationItem {
	readonly id: string;
	readonly name: string;
	protected discriminator: ResultType;
	readonly type: undefined | ps.NamedEntityType;
	readonly user_id: string;
	public score: ps.Score;
	public correct: boolean;
	public showMore: boolean;
	readonly item_id: string;
	readonly title: TitleData;
	readonly case_id: string;

	constructor(item: ps.KeywordRead | ps.NamedEntityRead, titles: TitleData[], case_id = '') {
		this.id = item.id;
		this.user_id = $(user).id;
		this.showMore = false;
		this.item_id = item.item_id;
		this.title = titles.find((title) => title.item_id == this.item_id);
		this.case_id = case_id;

		if (isKeyword(item)) {
			this.name = item.keyword;
			this.type = undefined;
			this.discriminator = ResultType.Keyword;
		} else {
			this.name = item.label;
			this.type = item.type;
			this.discriminator = ResultType.NamedEntity;
		}
	}

	isKeyword() {
		return this.discriminator === ResultType.Keyword;
	}

	getEvaluationType() {
		return this.isKeyword()
			? EvaluationType.ScoredEvaluation
			: EvaluationType.CorrectnessEvaluation;
	}

	getTypeName() {
		return NAMED_ENTITY_TO_WORD_WITH_ARTICLE[this.type];
	}

	getClasses() {
		const keywordClasses = ['keyword'];
		const namedEntityClasses = ['named-entity', this.type];
		const classes = this.isKeyword() ? keywordClasses : namedEntityClasses;
		return classes.join(' ');
	}

	getItem(readReports: ps.ReportWithPoints[]) {
		return readReports
			.flatMap((report) => report.item_results)
			.find((result) => result.id == this.id);
	}
	getDocument(readDocuments: ps.DocumentReadWithoutCases[] | ps.DocumentRead[]) {
		return readDocuments.find((readDocument) => readDocument.id === this.title.document_id);
	}

	getText(readDocuments: ps.DocumentReadWithoutCases[] | ps.DocumentRead[]): ps.TextRead {
		return readDocuments
			.flatMap((readDocument) => readDocument.items)
			.find((item) => item.id === this.item_id);
	}

	getResults(readReports: ps.ReportWithPoints[]) {
		return readReports
			.filter((readReport) => readReport.item_id == this.item_id)
			.flatMap((readReport) => readReport.item_results);
	}
	getDocumentLink(short: boolean = false) {
		const withContext = this.case_id === '' ? '' : '/context/' + this.case_id;

		let shortTitle = this.title.title;
		if (short === true) {
			shortTitle = getShortIfNeeded(this.title.title);
		}

		const link = `<a href="/dashboard/document/${this.title.document_id}${withContext}" target="new" sveltekit:prefetch>${shortTitle}</a>`;

		return link;
	}

	setValueFromBatch(value: ps.Score) {
		if (this.getEvaluationType() === EvaluationType.CorrectnessEvaluation) {
			return this.setValue(value > 0);
		}
		return this.setValue(value);
	}

	setValue(value: boolean | ps.Score) {
		const evaluationType = this.getEvaluationType();

		if (evaluationType === EvaluationType.CorrectnessEvaluation) {
			if (typeof value === 'boolean') {
				value = <boolean>value;
				this.correct = value;
				return;
			} else {
				throw new Error(`value (${value}) must be boolean, but isn't (${this})`);
			}
		}

		if (evaluationType === EvaluationType.ScoredEvaluation) {
			const isValidScore = value >= 0 && value <= 2;
			if (isValidScore) {
				value = <ps.Score>value;
				this.score = value;
				return;
			} else {
				throw new Error(`value (${value}) must be Score, but isn't (${this})`);
			}
		}
	}

	getEvaluationData() {
		const evaluationType = this.getEvaluationType();

		if (evaluationType === EvaluationType.CorrectnessEvaluation) {
			if (this?.correct === undefined) {
				throw new Error(`'correct' is not set (${this})`);
			} else {
				const data: ps.CorrectnessEvaluationCreate = {
					value: this.correct,
					discriminator: evaluationType
				};
				return data;
			}
		}

		if (evaluationType === EvaluationType.ScoredEvaluation && this?.score === undefined) {
			throw new Error(`'score' is not set (${this})`);
		}

		const data: ps.ScoredEvaluationCreate = { value: this.score, discriminator: evaluationType };
		return data;
	}
}
