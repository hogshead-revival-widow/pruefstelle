/* eslint-disable */
/* tslint:disable */
/*
 * ---------------------------------------------------------------
 * ## THIS FILE WAS GENERATED VIA SWAGGER-TYPESCRIPT-API        ##
 * ##                                                           ##
 * ## AUTHOR: acacode                                           ##
 * ## SOURCE: https://github.com/acacode/swagger-typescript-api ##
 * ---------------------------------------------------------------
 */

/*
  Modifications:
  renamed "data-contracts" -> "contracts"
  added AnyResult
*/

export type AnyResult = KeywordRead | NamedEntityRead | (KeywordRead & NamedEntityRead);

export interface AnyItemRead {
	/**
	 * Date
	 * @format date-time
	 */
	date: string;

	/**
	 * Document Id
	 * @format uuid
	 */
	document_id: string;
	source_category: CategoryRead;

	/** Parents */
	parents: string[];

	/** Mining Results */
	mining_results: (KeywordRead | NamedEntityRead | (KeywordRead & NamedEntityRead))[];

	/** Mining Jobs */
	mining_jobs: JobRead[];

	/** Research Quality Snapshots */
	research_quality_snapshots: SnapshotReadWithoutProfile[];

	/**
	 * Id
	 * @format uuid
	 */
	id: string;

	/** Discriminator */
	discriminator: 'item';
}

export interface BodyCreateTextApiTextPost {
	text: TextCreate;
	services: TextWorkflow[];
}

export interface BodyImportDocumentsWithTextsFromFesadExcelCollectionApiTaskFesadExcelCollectionPost {
	/**
	 * Excel Collection
	 * @format binary
	 */
	excel_collection: File;
}

export interface BodyLoginApiAuthLoginPost {
	/**
	 * Grant Type
	 * @pattern password
	 */
	grant_type?: string;

	/** Username */
	username: string;

	/** Password */
	password: string;

	/** Scope */
	scope?: string;

	/** Client Id */
	client_id?: string;

	/** Client Secret */
	client_secret?: string;
}

export interface CaseCreate {
	/** Title */
	title: string;

	/**
	 * Category Id
	 * @format uuid
	 */
	category_id: string;

	/**
	 * Original Case Id
	 * @format uuid
	 */
	original_case_id?: string;
	profile: ProfileCreate;

	/** Documents */
	documents: string[];
}

export interface CaseRead {
	/** Title */
	title: string;

	/**
	 * Date
	 * @format date-time
	 */
	date: string;

	/**
	 * Id
	 * @format uuid
	 */
	id: string;

	/**
	 * Original Case Id
	 * @format uuid
	 */
	original_case_id?: string;
	category: CategoryRead;
	profile: ProfileRead;

	/** Watchers */
	watchers: IDRead[];

	/** Documents */
	documents: DocumentReadWithoutCases[];
}

export interface CaseUpdate {
	/** Title */
	title: string;

	/**
	 * Original Case Id
	 * @format uuid
	 */
	original_case_id?: string;

	/**
	 * Category Id
	 * @format uuid
	 */
	category_id?: string;

	/** Documents */
	documents: string[];
}

export interface CategoryRead {
	/**
	 * Id
	 * @format uuid
	 */
	id: string;

	/** Name */
	name: string;
	source?: ChildCategoryRead;

	/** Discriminator */
	discriminator: string;

	/** Ndb Norm Id */
	ndb_norm_id?: number;
}

/**
 * An enumeration.
 */
export enum CategoryType {
	CaseCategory = 'case_category',
	DocumentCategory = 'document_category',
	SourceCategory = 'source_category',
	ExternalIdCategory = 'external_id_category',
	TextCategory = 'text_category'
}

export interface ChildCategoryRead {
	/**
	 * Id
	 * @format uuid
	 */
	id: string;

	/** Name */
	name: string;

	/** Discriminator */
	discriminator: string;

	/** Ndb Norm Id */
	ndb_norm_id?: number;
}

export interface Constraint {
	/** Constraint Name */
	constraint_name: string;

	/** Expected Value */
	expected_value: number;

	/** Found Value */
	found_value: number;
}

export interface CorrectnessEvaluationCreate {
	/** Discriminator */
	discriminator: 'correctness_evaluation';

	/** Value */
	value: boolean;
}

export interface DocumentCreate {
	/** Title */
	title: string;

	/**
	 * Category Id
	 * @format uuid
	 */
	category_id: string;

	/** External Id */
	external_id?: string;

	/**
	 * External Id Category Id
	 * @format uuid
	 */
	external_id_category_id?: string;

	/** Cases */
	cases: string[];
}

export interface DocumentRead {
	/** Title */
	title: string;

	/**
	 * Date
	 * @format date-time
	 */
	date: string;
	category: CategoryRead;

	/** External Id */
	external_id?: string;
	external_id_category?: CategoryRead;

	/** Items */
	items: TextRead[];

	/**
	 * Id
	 * @format uuid
	 */
	id: string;

	/** Cases */
	cases: IDTitleRead[];
}

export interface DocumentReadWithoutCases {
	/** Title */
	title: string;

	/**
	 * Date
	 * @format date-time
	 */
	date: string;
	category: CategoryRead;

	/** External Id */
	external_id?: string;
	external_id_category?: CategoryRead;

	/** Items */
	items: TextRead[];

	/**
	 * Id
	 * @format uuid
	 */
	id: string;
}

export interface DocumentUpdate {
	/** Title */
	title?: string;

	/**
	 * Category Id
	 * @format uuid
	 */
	category_id?: string;

	/** External Id */
	external_id?: string;

	/**
	 * External Id Category Id
	 * @format uuid
	 */
	external_id_category_id?: string;
}

export interface EvaluationRead {
	/**
	 * Date
	 * @format date-time
	 */
	date: string;

	/**
	 * Creator Id
	 * @format uuid
	 */
	creator_id: string;

	/**
	 * Id
	 * @format uuid
	 */
	id: string;

	/**
	 * Mining Result Id
	 * @format uuid
	 */
	mining_result_id: string;

	/** Value */
	value: number;

	/** An enumeration. */
	discriminator: EvaluationType;

	/** Is Good */
	is_good?: boolean;
}

/**
 * An enumeration.
 */
export enum EvaluationType {
	ScoredEvaluation = 'scored_evaluation',
	CorrectnessEvaluation = 'correctness_evaluation'
}

export interface HTTPValidationError {
	/** Detail */
	detail?: ValidationError[];
}

export interface IDRead {
	/**
	 * Id
	 * @format uuid
	 */
	id: string;
}

export interface IDTitleRead {
	/** Title */
	title: string;

	/**
	 * Id
	 * @format uuid
	 */
	id: string;
}

export interface JobRead {
	/**
	 * Date
	 * @format date-time
	 */
	date: string;

	/** An enumeration. */
	status: Status;

	/** An enumeration. */
	service: TextWorkflow;

	/** External Id */
	external_id?: string;

	/**
	 * Item Id
	 * @format uuid
	 */
	item_id: string;

	/**
	 * Id
	 * @format uuid
	 */
	id: string;
}

export interface KeywordCreate {
	/**
	 * Item Id
	 * @format uuid
	 */
	item_id: string;

	/** Keyword */
	keyword: string;

	/** Relevance */
	relevance: number;

	/** Frequency */
	frequency: number;

	/** Confidence */
	confidence: number;

	/** Discriminator */
	discriminator: 'result_keyword';
}

export interface KeywordRead {
	/**
	 * Id
	 * @format uuid
	 */
	id: string;

	/**
	 * Date
	 * @format date-time
	 */
	date: string;

	/**
	 * Item Id
	 * @format uuid
	 */
	item_id: string;

	/** Evaluations */
	evaluations: EvaluationRead[];

	/** Keyword */
	keyword: string;

	/** Relevance */
	relevance: number;

	/** Frequency */
	frequency: number;

	/** Confidence */
	confidence: number;

	/** Discriminator */
	discriminator: 'result_keyword';
}

export interface NamedEntityCreate {
	/**
	 * Item Id
	 * @format uuid
	 */
	item_id: string;

	/** An enumeration. */
	type: NamedEntityType;

	/** Label */
	label: string;

	/** Begin */
	begin: number;

	/** End */
	end: number;

	/** Discriminator */
	discriminator: 'result_named_entity';
}

export interface NamedEntityRead {
	/**
	 * Id
	 * @format uuid
	 */
	id: string;

	/**
	 * Date
	 * @format date-time
	 */
	date: string;

	/**
	 * Item Id
	 * @format uuid
	 */
	item_id: string;

	/** Evaluations */
	evaluations: EvaluationRead[];

	/** An enumeration. */
	type: NamedEntityType;

	/** Label */
	label: string;

	/** Begin */
	begin: number;

	/** End */
	end: number;

	/** Discriminator */
	discriminator: 'result_named_entity';
}

/**
 * An enumeration.
 */
export enum NamedEntityType {
	PERSON = 'PERSON',
	LOCATION = 'LOCATION',
	ORGANIZATION = 'ORGANIZATION'
}

export interface PageCaseRead {
	/** Items */
	items: CaseRead[];

	/**
	 * Total
	 * @min 0
	 */
	total: number;

	/**
	 * Page
	 * @min 1
	 */
	page: number;

	/**
	 * Size
	 * @min 1
	 */
	size: number;
}

export interface PageEvaluationRead {
	/** Items */
	items: EvaluationRead[];

	/**
	 * Total
	 * @min 0
	 */
	total: number;

	/**
	 * Page
	 * @min 1
	 */
	page: number;

	/**
	 * Size
	 * @min 1
	 */
	size: number;
}

export interface PageUUID {
	/** Items */
	items: string[];

	/**
	 * Total
	 * @min 0
	 */
	total: number;

	/**
	 * Page
	 * @min 1
	 */
	page: number;

	/**
	 * Size
	 * @min 1
	 */
	size: number;
}

export interface ProfileCreate {
	/**
	 * Keyword Relevance Threshold
	 * @min 0
	 */
	keyword_relevance_threshold?: number;

	/**
	 * Keyword Confidence Threshold
	 * @min 0
	 */
	keyword_confidence_threshold?: number;

	/**
	 * Keyword Frequency Threshold
	 * @min 0
	 */
	keyword_frequency_threshold?: number;

	/**
	 * Keyword Only Top N Relevance
	 * @min 0
	 */
	keyword_only_top_n_relevance?: number;

	/**
	 * Research Quality Constraint Needed Users
	 * @min 1
	 */
	research_quality_constraint_needed_users?: number;

	/**
	 * Research Quality Good Threshold
	 * @min 50
	 */
	research_quality_good_threshold?: number;
}

export interface ProfileRead {
	/**
	 * Keyword Only Top N Relevance
	 * @min 0
	 */
	keyword_only_top_n_relevance?: number;

	/**
	 * Keyword Relevance Threshold
	 * @min 0
	 */
	keyword_relevance_threshold?: number;

	/**
	 * Keyword Confidence Threshold
	 * @min 0
	 */
	keyword_confidence_threshold?: number;

	/**
	 * Keyword Frequency Threshold
	 * @min 0
	 */
	keyword_frequency_threshold?: number;

	/**
	 * Research Quality Good Threshold
	 * @min 50
	 */
	research_quality_good_threshold?: number;

	/**
	 * Research Quality Constraint Needed Users
	 * @min 1
	 */
	research_quality_constraint_needed_users?: number;

	/**
	 * Id
	 * @format uuid
	 */
	id: string;
}

export interface ProfileUpdate {
	/**
	 * Keyword Relevance Threshold
	 * @min 0
	 */
	keyword_relevance_threshold?: number;

	/**
	 * Keyword Confidence Threshold
	 * @min 0
	 */
	keyword_confidence_threshold?: number;

	/**
	 * Keyword Frequency Threshold
	 * @min 0
	 */
	keyword_frequency_threshold?: number;

	/**
	 * Keyword Only Top N Relevance
	 * @min 0
	 */
	keyword_only_top_n_relevance?: number;

	/**
	 * Research Quality Constraint Needed Users
	 * @min 1
	 */
	research_quality_constraint_needed_users?: number;

	/**
	 * Research Quality Good Threshold
	 * @min 50
	 */
	research_quality_good_threshold?: number;
}

export interface ReportWithPoints {
	/** Points */
	points: number;

	/** Item Results Calculation Conditions Met */
	item_results_calculation_conditions_met: boolean;

	/** Optioned Results Calculation Conditions Met */
	optioned_results_calculation_conditions_met: boolean;

	/**
	 * Item Id
	 * @format uuid
	 */
	item_id: string;

	/**
	 * Profile Id
	 * @format uuid
	 */
	profile_id: string;

	/** Item Results */
	item_results: (KeywordRead | NamedEntityRead | (KeywordRead & NamedEntityRead))[];

	/**
	 * Item Results Total
	 * @min 0
	 */
	item_results_total: number;

	/**
	 * Item Results Min Unique Creators
	 * @min 0
	 */
	item_results_min_unique_creators: number;

	/**
	 * Optioned Results Min Unique Creators
	 * @min 0
	 */
	optioned_results_min_unique_creators: number;

	/** Item Results All Evaluated */
	item_results_all_evaluated: boolean;

	/** Optioned Results All Evaluated */
	optioned_results_all_evaluated: boolean;

	/**
	 * Optioned Results Total
	 * @min 0
	 */
	optioned_results_total: number;

	/** Optioned Results By Id */
	optioned_results_by_id: string[];

	/**
	 * Item Results Ignored By Option
	 * @min 0
	 */
	item_results_ignored_by_option: number;

	/** Item Results Failed Constraints */
	item_results_failed_constraints: Constraint[];

	/** Optioned Results Failed Constraints */
	optioned_results_failed_constraints: Constraint[];
}

export interface ResultCreate {
	/** Result */
	result: KeywordCreate | NamedEntityCreate | (KeywordCreate & NamedEntityCreate);
}

/**
 * An enumeration.
 */
export type Score = 0 | 1 | 2;

export interface ScoredEvaluationCreate {
	/** Discriminator */
	discriminator: 'scored_evaluation';

	/** An enumeration. */
	value: Score;
}

export interface SnapshotRead {
	/**
	 * Date
	 * @format date-time
	 */
	date: string;

	/** Points */
	points: number;

	/**
	 * Item Id
	 * @format uuid
	 */
	item_id: string;

	/**
	 * Id
	 * @format uuid
	 */
	id: string;
	profile: ProfileRead;
}

export interface SnapshotReadWithoutProfile {
	/**
	 * Date
	 * @format date-time
	 */
	date: string;

	/** Points */
	points: number;

	/**
	 * Item Id
	 * @format uuid
	 */
	item_id: string;

	/**
	 * Id
	 * @format uuid
	 */
	id: string;
}

/**
 * An enumeration.
 */
export enum Status {
	DRAFT = 'DRAFT',
	TO_BE_STARTED = 'TO_BE_STARTED',
	WAITING_FOR_RETURN = 'WAITING_FOR_RETURN',
	NON_API_ERROR = 'NON_API_ERROR',
	RESULTS_IN_DB = 'RESULTS_IN_DB',
	NEW = 'NEW',
	RUNNING = 'RUNNING',
	PARTIALLY_COMPLETED = 'PARTIALLY_COMPLETED',
	COMPLETED = 'COMPLETED',
	FAILED = 'FAILED'
}

export interface TextCreate {
	/** Content */
	content: string;

	/**
	 * Document Id
	 * @format uuid
	 */
	document_id: string;

	/**
	 * Source Category Id
	 * @format uuid
	 */
	source_category_id: string;

	/**
	 * Category Id
	 * @format uuid
	 */
	category_id: string;

	/** Parents */
	parents: string[];
}

export interface TextRead {
	/** Title */
	title: string;

	/**
	 * Date
	 * @format date-time
	 */
	date: string;

	/**
	 * Document Id
	 * @format uuid
	 */
	document_id: string;
	source_category: CategoryRead;

	/** Parents */
	parents: string[];

	/** Mining Results */
	mining_results: (KeywordRead | NamedEntityRead | (KeywordRead & NamedEntityRead))[];

	/** Mining Jobs */
	mining_jobs: JobRead[];

	/** Research Quality Snapshots */
	research_quality_snapshots: SnapshotReadWithoutProfile[];

	/** Content */
	content: string;
	category: CategoryRead;

	/** Discriminator */
	discriminator: 'text';

	/**
	 * Id
	 * @format uuid
	 */
	id: string;
}

export interface TextUpdate {
	/**
	 * Source Category Id
	 * @format uuid
	 */
	source_category_id?: string;

	/**
	 * Category Id
	 * @format uuid
	 */
	category_id?: string;

	/**
	 * Document Id
	 * @format uuid
	 */
	document_id?: string;
}

/**
 * An enumeration.
 */
export enum TextWorkflow {
	KeywordExtraction = 'keyword-extraction',
	NamedEntityRecognition = 'named-entity-recognition'
}

export interface UserRead {
	/**
	 * Email
	 * @format email
	 */
	email: string;

	/** Superuser */
	superuser: boolean;

	/**
	 * Id
	 * @format uuid
	 */
	id: string;
}

export interface UserUpdate {
	/** Current Password */
	current_password: string;

	/**
	 * Email
	 * @format email
	 */
	email?: string;

	/** New Password */
	new_password?: string;
}

export interface ValidationError {
	/** Location */
	loc: (string | number)[];

	/** Message */
	msg: string;

	/** Error Type */
	type: string;
}
