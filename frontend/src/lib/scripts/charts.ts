import { ps, isKeyword, type ItemInformation, ResultType } from '$lib/api';
import { NAMED_ENTITY_TO_WORD } from '$lib/data/namedEntities';

interface ChartItem extends ItemInformation {
	good: number;
	bad: number;
}

export type Dataset = { good: { x: string; y: number }[]; bad: { x: string; y: number }[] };

export type DatasetWithMeta = { title: string; dataset: Dataset; titleClasses: string[] };

const itemToChartInformation = (item: ps.AnyResult): ChartItem => {
	const good = item.evaluations.filter((evaluation) => evaluation.is_good).length;
	const bad = item.evaluations.filter((evaluation) => !evaluation.is_good).length;

	if (isKeyword(item)) {
		return {
			id: item.id,
			name: 'Keyword: ' + item.keyword,
			discriminator: ResultType.Keyword,
			type: undefined,
			good: good,
			bad: bad
		};
	}
	return {
		id: item.id,
		name: `${NAMED_ENTITY_TO_WORD[item.type]}: ` + item.label,
		discriminator: ResultType.NamedEntity,
		type: item.type,
		good: good,
		bad: bad
	};
};
const itemsToDataset = (items: ps.AnyResult[]): Dataset => {
	const infos: ChartItem[] = items
		.filter((item) => item.evaluations.length > 0)
		.map((item) => itemToChartInformation(item));

	const good = infos
		.filter((info) => info.good > 0)
		.map((info) => ({ x: info.name, y: info.good }));
	const bad = infos.filter((info) => info.bad > 0).map((info) => ({ x: info.name, y: info.bad }));
	return { good, bad };
};

export const getCharts = (readReports: ps.ReportWithPoints[] | undefined) => {
	const charts: DatasetWithMeta[] = [];

	if (readReports === undefined) return charts;

	const allItems = readReports.flatMap((report) => report.item_results);

	const keywords = allItems.filter((item) => isKeyword(item));
	if (keywords.length > 0) {
		const keywordData: DatasetWithMeta = {
			title: 'Keywords',
			dataset: itemsToDataset(keywords),
			titleClasses: ['keyword']
		};
		charts.push(keywordData);
	}

	const namedEntites = allItems.filter((item) => !isKeyword(item));

	if (namedEntites.length > 0) {
		const namedEntityData: DatasetWithMeta = {
			title: 'Entitäten',
			dataset: itemsToDataset(namedEntites),
			titleClasses: ['named-entity']
		};
		charts.push(namedEntityData);
	}

	return charts;
};
