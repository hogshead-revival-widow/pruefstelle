import * as ps from './contracts';
import { makePruefstelle, Pruefstelle } from './client';
import { isKeyword, isEntity, isTopic, isText, isCase, isDocument } from './utils';

export {
	ps,
	makePruefstelle,
	Pruefstelle,
	isKeyword,
	isEntity,
	isText,
	isTopic,
	isCase,
	isDocument
};

export enum ResultType {
	Keyword = 'result_keyword',
	NamedEntity = 'result_named_entity',
	Topic = 'topic'
}

export const EvaluationType = ps.EvaluationType;
export const NamedEntityType = ps.NamedEntityType;
export const CategoryType = ps.CategoryType;

export const TextWorkflow = ps.TextWorkflow;
export type RelevantCategory =
	| ps.CategoryType.CaseCategory
	| ps.CategoryType.DocumentCategory
	| ps.CategoryType.TextCategory
	| ps.CategoryType.SourceCategory
	| ps.CategoryType.ExternalIdCategory;

export type CategoriesByType = Record<RelevantCategory, ps.CategoryRead[]>;

export interface ItemInformation {
	id: string;
	name: string;
	discriminator: ResultType.Keyword | ResultType.NamedEntity | ResultType.Topic;
	type: undefined | ps.NamedEntityType;
}
