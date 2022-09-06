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
  18: renamed "data-contracts" -> "contracts"
  18: all imports from "./contracts" must be imported with `type` keyword
  51: import `RequestParams` from "./http-client" must be imported with `type` keyword
*/

import type {
	BodyCreateTextApiTextPost,
	BodyImportDocumentsWithTextsFromFesadExcelCollectionApiTaskFesadExcelCollectionPost,
	BodyLoginApiAuthLoginPost,
	CaseCreate,
	CaseRead,
	CaseUpdate,
	CategoryRead,
	CategoryType,
	CorrectnessEvaluationCreate,
	DocumentCreate,
	DocumentRead,
	DocumentUpdate,
	EvaluationRead,
	HTTPValidationError,
	JobRead,
	KeywordRead,
	NamedEntityRead,
	PageCaseRead,
	PageEvaluationRead,
	PageUUID,
	ProfileRead,
	ProfileUpdate,
	ReportWithPoints,
	ResultCreate,
	ScoredEvaluationCreate,
	SnapshotRead,
	TextRead,
	TextUpdate,
	TextWorkflow,
	UserRead,
	UserUpdate
} from './contracts';
import { ContentType, HttpClient, type RequestParams } from './http-client';

export class Api<SecurityDataType = unknown> {
	http: HttpClient<SecurityDataType>;

	constructor(http: HttpClient<SecurityDataType>) {
		this.http = http;
	}

	/**
	 * No description
	 *
	 * @tags Case
	 * @name ListCases
	 * @summary List Cases
	 * @request GET:/api/case
	 * @secure
	 */
	listCases = (query?: { page?: number; size?: number }, params: RequestParams = {}) =>
		this.http.request<PageCaseRead, HTTPValidationError>({
			path: `/api/case`,
			method: 'GET',
			query: query,
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * No description
	 *
	 * @tags Case
	 * @name CreateCase
	 * @summary Create Case
	 * @request POST:/api/case
	 * @secure
	 */
	createCase = (data: CaseCreate, params: RequestParams = {}) =>
		this.http.request<CaseRead, HTTPValidationError>({
			path: `/api/case`,
			method: 'POST',
			body: data,
			secure: true,
			type: ContentType.Json,
			format: 'json',
			...params
		});
	/**
	 * @description Search for a case that has a matching category name or title.
	 *
	 * @tags Case
	 * @name SearchCases
	 * @summary Search Cases
	 * @request GET:/api/case/search
	 * @secure
	 */
	searchCases = (
		query?: { title?: string; category_name?: string; page?: number; size?: number },
		params: RequestParams = {}
	) =>
		this.http.request<PageUUID, HTTPValidationError>({
			path: `/api/case/search`,
			method: 'GET',
			query: query,
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * No description
	 *
	 * @tags Case
	 * @name ReadCase
	 * @summary Read Case
	 * @request GET:/api/case/{case_id}
	 * @secure
	 */
	readCase = (caseId: string, params: RequestParams = {}) =>
		this.http.request<CaseRead, HTTPValidationError>({
			path: `/api/case/${caseId}`,
			method: 'GET',
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * @description Note: - You can only delete a case if - it was created by you and - it has no documents attached yet
	 *
	 * @tags Case
	 * @name DeleteCase
	 * @summary Delete Case
	 * @request DELETE:/api/case/{case_id}
	 * @secure
	 */
	deleteCase = (caseId: string, params: RequestParams = {}) =>
		this.http.request<CaseRead, HTTPValidationError>({
			path: `/api/case/${caseId}`,
			method: 'DELETE',
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * @description Note: - You can only update a case if - it was created by you and - it has no documents attached yet
	 *
	 * @tags Case
	 * @name UpdateCase
	 * @summary Update Case
	 * @request PATCH:/api/case/{case_id}
	 * @secure
	 */
	updateCase = (caseId: string, data: CaseUpdate, params: RequestParams = {}) =>
		this.http.request<CaseRead, HTTPValidationError>({
			path: `/api/case/${caseId}`,
			method: 'PATCH',
			body: data,
			secure: true,
			type: ContentType.Json,
			format: 'json',
			...params
		});
	/**
	 * No description
	 *
	 * @tags Document
	 * @name CreateDocument
	 * @summary Create Document
	 * @request POST:/api/document
	 * @secure
	 */
	createDocument = (data: DocumentCreate, params: RequestParams = {}) =>
		this.http.request<DocumentRead, HTTPValidationError>({
			path: `/api/document`,
			method: 'POST',
			body: data,
			secure: true,
			type: ContentType.Json,
			format: 'json',
			...params
		});
	/**
	 * No description
	 *
	 * @tags Document
	 * @name ReadDocumentFromMiningResult
	 * @summary Read Document From Mining Result
	 * @request GET:/api/document/mining_result/{mining_result_id}
	 * @secure
	 */
	readDocumentFromMiningResult = (miningResultId: string, params: RequestParams = {}) =>
		this.http.request<DocumentRead, HTTPValidationError>({
			path: `/api/document/mining_result/${miningResultId}`,
			method: 'GET',
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * No description
	 *
	 * @tags Document
	 * @name ReadDocument
	 * @summary Read Document
	 * @request GET:/api/document/{document_id}
	 * @secure
	 */
	readDocument = (documentId: string, params: RequestParams = {}) =>
		this.http.request<DocumentRead, HTTPValidationError>({
			path: `/api/document/${documentId}`,
			method: 'GET',
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * @description Beware: - This will also delete any items (e.g. texts) attached to this document Note: - You can only delete a document if - it was created by you and - it has no cases attached yet
	 *
	 * @tags Document
	 * @name DeleteDocument
	 * @summary Delete Document
	 * @request DELETE:/api/document/{document_id}
	 * @secure
	 */
	deleteDocumentAndDependingItems = (documentId: string, params: RequestParams = {}) =>
		this.http.request<CaseRead, HTTPValidationError>({
			path: `/api/document/${documentId}`,
			method: 'DELETE',
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * @description Note: - You can only update a document if - it was created by you and - it has no cases attached yet
	 *
	 * @tags Document
	 * @name UpdateDocument
	 * @summary Update Document
	 * @request PATCH:/api/document/{document_id}
	 * @secure
	 */
	updateDocument = (documentId: string, data: DocumentUpdate, params: RequestParams = {}) =>
		this.http.request<DocumentRead, HTTPValidationError>({
			path: `/api/document/${documentId}`,
			method: 'PATCH',
			body: data,
			secure: true,
			type: ContentType.Json,
			format: 'json',
			...params
		});
	/**
	 * @description Create a text and a job for every service specified and start the jobs. Note: You need to create a document before adding a text.
	 *
	 * @tags Text
	 * @name CreateText
	 * @summary Create Text
	 * @request POST:/api/text
	 * @secure
	 */
	createText = (data: BodyCreateTextApiTextPost, params: RequestParams = {}) =>
		this.http.request<TextRead, HTTPValidationError>({
			path: `/api/text`,
			method: 'POST',
			body: data,
			secure: true,
			type: ContentType.Json,
			format: 'json',
			...params
		});
	/**
	 * No description
	 *
	 * @tags Text
	 * @name ReadText
	 * @summary Read Text
	 * @request GET:/api/text/{text_id}
	 * @secure
	 */
	readText = (textId: string, params: RequestParams = {}) =>
		this.http.request<TextRead, HTTPValidationError>({
			path: `/api/text/${textId}`,
			method: 'GET',
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * @description Note: - You can only delete a text, if - it was created by you and - the document it is attached to is not used in any case
	 *
	 * @tags Text
	 * @name DeleteText
	 * @summary Delete Text
	 * @request DELETE:/api/text/{text_id}
	 * @secure
	 */
	deleteText = (textId: string, params: RequestParams = {}) =>
		this.http.request<TextRead, HTTPValidationError>({
			path: `/api/text/${textId}`,
			method: 'DELETE',
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * @description Note: - You can only update a text, if - it was created by you and - the document it is attached to is not used in any case
	 *
	 * @tags Text
	 * @name UpdateText
	 * @summary Update Text
	 * @request PATCH:/api/text/{text_id}
	 * @secure
	 */
	updateText = (textId: string, data: TextUpdate, params: RequestParams = {}) =>
		this.http.request<TextRead, HTTPValidationError>({
			path: `/api/text/${textId}`,
			method: 'PATCH',
			body: data,
			secure: true,
			type: ContentType.Json,
			format: 'json',
			...params
		});
	/**
	 * No description
	 *
	 * @tags Evaluation
	 * @name ReadItemEvaluations
	 * @summary Read Item Evaluations
	 * @request GET:/api/evaluation/mining_result/{mining_result_id}
	 * @secure
	 */
	readItemEvaluations = (miningResultId: string, params: RequestParams = {}) =>
		this.http.request<EvaluationRead[], HTTPValidationError>({
			path: `/api/evaluation/mining_result/${miningResultId}`,
			method: 'GET',
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * No description
	 *
	 * @tags Evaluation
	 * @name CreateEvaluation
	 * @summary Create Evaluation
	 * @request POST:/api/evaluation/mining_result/{mining_result_id}
	 * @secure
	 */
	createEvaluation = (
		miningResultId: string,
		data:
			| ScoredEvaluationCreate
			| CorrectnessEvaluationCreate
			| (ScoredEvaluationCreate & CorrectnessEvaluationCreate),
		params: RequestParams = {}
	) =>
		this.http.request<EvaluationRead, HTTPValidationError>({
			path: `/api/evaluation/mining_result/${miningResultId}`,
			method: 'POST',
			body: data,
			secure: true,
			type: ContentType.Json,
			format: 'json',
			...params
		});
	/**
	 * No description
	 *
	 * @tags Evaluation
	 * @name ReadEvaluation
	 * @summary Read Evaluation
	 * @request GET:/api/evaluation/{evaluation_id}
	 * @secure
	 */
	readEvaluation = (evaluationId: string, params: RequestParams = {}) =>
		this.http.request<EvaluationRead, HTTPValidationError>({
			path: `/api/evaluation/${evaluationId}`,
			method: 'GET',
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * @description You can only delete an evaluation, if it was created by you
	 *
	 * @tags Evaluation
	 * @name DeleteEvaluation
	 * @summary Delete Evaluation
	 * @request DELETE:/api/evaluation/{evaluation_id}
	 * @secure
	 */
	deleteEvaluation = (evaluationId: string, params: RequestParams = {}) =>
		this.http.request<EvaluationRead, HTTPValidationError>({
			path: `/api/evaluation/${evaluationId}`,
			method: 'DELETE',
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * @description You can only update an evaluation, if it was created by you
	 *
	 * @tags Evaluation
	 * @name UpdateEvaluation
	 * @summary Update Evaluation
	 * @request PATCH:/api/evaluation/{evaluation_id}
	 * @secure
	 */
	updateEvaluation = (
		evaluationId: string,
		data:
			| ScoredEvaluationCreate
			| CorrectnessEvaluationCreate
			| (ScoredEvaluationCreate & CorrectnessEvaluationCreate),
		params: RequestParams = {}
	) =>
		this.http.request<EvaluationRead, HTTPValidationError>({
			path: `/api/evaluation/${evaluationId}`,
			method: 'PATCH',
			body: data,
			secure: true,
			type: ContentType.Json,
			format: 'json',
			...params
		});
	/**
	 * @description Points for all items (e.g.texts)  of a case
	 *
	 * @tags Report
	 * @name ReadCaseReport
	 * @summary Read Case Report
	 * @request GET:/api/report/case/{case_id}
	 * @secure
	 */
	readCaseReport = (caseId: string, params: RequestParams = {}) =>
		this.http.request<ReportWithPoints[], HTTPValidationError>({
			path: `/api/report/case/${caseId}`,
			method: 'GET',
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * @description Points for all items (e.g.texts)  of a document
	 *
	 * @tags Report
	 * @name ReadDocumentReport
	 * @summary Read Document Report
	 * @request GET:/api/report/case/{case_id}/document/{document_id}
	 * @secure
	 */
	readDocumentReport = (documentId: string, caseId: string, params: RequestParams = {}) =>
		this.http.request<ReportWithPoints[], HTTPValidationError>({
			path: `/api/report/case/${caseId}/document/${documentId}`,
			method: 'GET',
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * @description Points for item (e.g. a text)
	 *
	 * @tags Report
	 * @name ReadItemReport
	 * @summary Read Item Report
	 * @request GET:/api/report/case/{case_id}/item/{item_id}
	 * @secure
	 */
	readItemReport = (itemId: string, caseId: string, params: RequestParams = {}) =>
		this.http.request<ReportWithPoints, HTTPValidationError>({
			path: `/api/report/case/${caseId}/item/${itemId}`,
			method: 'GET',
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * No description
	 *
	 * @tags Report
	 * @name ReadProfile
	 * @summary Read Profile
	 * @request GET:/api/report/profile/{profile_id}
	 * @secure
	 */
	readProfile = (profileId: string, params: RequestParams = {}) =>
		this.http.request<ProfileRead, HTTPValidationError>({
			path: `/api/report/profile/${profileId}`,
			method: 'GET',
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * No description
	 *
	 * @tags Report
	 * @name UpdateProfile
	 * @summary Update Profile
	 * @request PATCH:/api/report/profile/{profile_id}
	 * @secure
	 */
	updateProfile = (profileId: string, data: ProfileUpdate, params: RequestParams = {}) =>
		this.http.request<ProfileRead, HTTPValidationError>({
			path: `/api/report/profile/${profileId}`,
			method: 'PATCH',
			body: data,
			secure: true,
			type: ContentType.Json,
			format: 'json',
			...params
		});
	/**
	 * No description
	 *
	 * @tags Report
	 * @name ReadProfileFromCase
	 * @summary Read Profile From Case
	 * @request GET:/api/report/profile/{case_id}/case
	 * @secure
	 */
	readProfileFromCase = (caseId: string, params: RequestParams = {}) =>
		this.http.request<ProfileRead, HTTPValidationError>({
			path: `/api/report/profile/${caseId}/case`,
			method: 'GET',
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * No description
	 *
	 * @tags Report
	 * @name UpdateProfileFromCase
	 * @summary Update Profile From Case
	 * @request PATCH:/api/report/case/profile/{case_id}
	 * @secure
	 */
	updateProfileFromCase = (caseId: string, data: ProfileUpdate, params: RequestParams = {}) =>
		this.http.request<ProfileRead, HTTPValidationError>({
			path: `/api/report/case/profile/${caseId}`,
			method: 'PATCH',
			body: data,
			secure: true,
			type: ContentType.Json,
			format: 'json',
			...params
		});
	/**
	 * No description
	 *
	 * @tags Category
	 * @name ReadCategory
	 * @summary Read Category
	 * @request GET:/api/category/{category_id}
	 * @secure
	 */
	readCategory = (categoryId: string, params: RequestParams = {}) =>
		this.http.request<CategoryRead, HTTPValidationError>({
			path: `/api/category/${categoryId}`,
			method: 'GET',
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * No description
	 *
	 * @tags Category
	 * @name ListCategories
	 * @summary List Categories
	 * @request GET:/api/category/list/{category_type}
	 * @secure
	 */
	listCategories = (categoryType: CategoryType, params: RequestParams = {}) =>
		this.http.request<CategoryRead[], HTTPValidationError>({
			path: `/api/category/list/${categoryType}`,
			method: 'GET',
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * No description
	 *
	 * @tags User
	 * @name ReadSelf
	 * @summary Read Self
	 * @request GET:/api/user/self
	 * @secure
	 */
	readSelf = (params: RequestParams = {}) =>
		this.http.request<UserRead, any>({
			path: `/api/user/self`,
			method: 'GET',
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * No description
	 *
	 * @tags User
	 * @name UpdateSelf
	 * @summary Update Self
	 * @request PATCH:/api/user/self
	 * @secure
	 */
	updateSelf = (data: UserUpdate, params: RequestParams = {}) =>
		this.http.request<UserRead, HTTPValidationError>({
			path: `/api/user/self`,
			method: 'PATCH',
			body: data,
			secure: true,
			type: ContentType.Json,
			format: 'json',
			...params
		});
	/**
	 * No description
	 *
	 * @tags User
	 * @name ReadSelfCases
	 * @summary Read Self Cases
	 * @request GET:/api/user/self/cases
	 * @secure
	 */
	readSelfCases = (query?: { page?: number; size?: number }, params: RequestParams = {}) =>
		this.http.request<PageCaseRead, HTTPValidationError>({
			path: `/api/user/self/cases`,
			method: 'GET',
			query: query,
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * No description
	 *
	 * @tags User
	 * @name ReadSelfEvaluations
	 * @summary Read Self Evaluations
	 * @request GET:/api/user/self/evaluations
	 * @secure
	 */
	readSelfEvaluations = (query?: { page?: number; size?: number }, params: RequestParams = {}) =>
		this.http.request<PageEvaluationRead, HTTPValidationError>({
			path: `/api/user/self/evaluations`,
			method: 'GET',
			query: query,
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * No description
	 *
	 * @tags User
	 * @name ReadSelfEvaluationsForCase
	 * @summary Read Self Evaluations For Case
	 * @request GET:/api/user/self/evaluations/case/{case_id}
	 * @secure
	 */
	readSelfEvaluationsForCase = (
		caseId: string,
		query?: { page?: number; size?: number },
		params: RequestParams = {}
	) =>
		this.http.request<PageEvaluationRead, HTTPValidationError>({
			path: `/api/user/self/evaluations/case/${caseId}`,
			method: 'GET',
			query: query,
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * No description
	 *
	 * @tags User
	 * @name ReadSelfEvaluationsForDocument
	 * @summary Read Self Evaluations For Document
	 * @request GET:/api/user/self/evaluations/document/{document_id}
	 * @secure
	 */
	readSelfEvaluationsForDocument = (
		documentId: string,
		query?: { page?: number; size?: number },
		params: RequestParams = {}
	) =>
		this.http.request<PageEvaluationRead, HTTPValidationError>({
			path: `/api/user/self/evaluations/document/${documentId}`,
			method: 'GET',
			query: query,
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * No description
	 *
	 * @tags User
	 * @name ReadSelfEvaluationsForText
	 * @summary Read Self Evaluations For Text
	 * @request GET:/api/user/self/evaluations/text/{text_id}
	 * @secure
	 */
	readSelfEvaluationsForText = (
		textId: string,
		query?: { page?: number; size?: number },
		params: RequestParams = {}
	) =>
		this.http.request<PageEvaluationRead, HTTPValidationError>({
			path: `/api/user/self/evaluations/text/${textId}`,
			method: 'GET',
			query: query,
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * @description "Stop watching a case, if you watch it. Start watching it, if you don't.
	 *
	 * @tags User
	 * @name ToggleWatchCase
	 * @summary Toggle Watch Case
	 * @request POST:/api/user/self/watch/{case_id}
	 * @secure
	 */
	toggleWatchCase = (caseId: string, params: RequestParams = {}) =>
		this.http.request<CaseRead, HTTPValidationError>({
			path: `/api/user/self/watch/${caseId}`,
			method: 'POST',
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * No description
	 *
	 * @tags Mining Job
	 * @name ReadJob
	 * @summary Read Job
	 * @request GET:/api/job/{job_id}
	 * @secure
	 */
	readJob = (jobId: string, params: RequestParams = {}) =>
		this.http.request<JobRead, HTTPValidationError>({
			path: `/api/job/${jobId}`,
			method: 'GET',
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * @description Note: - You can only delete a job, if - it was created by you and - it is a draft
	 *
	 * @tags Mining Job
	 * @name DeleteJob
	 * @summary Delete Job
	 * @request DELETE:/api/job/{job_id}
	 * @secure
	 */
	deleteJob = (jobId: string, params: RequestParams = {}) =>
		this.http.request<JobRead, HTTPValidationError>({
			path: `/api/job/${jobId}`,
			method: 'DELETE',
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * @description Set a job, i.e. a job draft, to start. Note: - You can only update a job, if - it was created by you and - it is a draft
	 *
	 * @tags Mining Job
	 * @name StartJob
	 * @summary Start Job
	 * @request PATCH:/api/job/{job_id}/start
	 * @secure
	 */
	startJob = (jobId: string, params: RequestParams = {}) =>
		this.http.request<JobRead, HTTPValidationError>({
			path: `/api/job/${jobId}/start`,
			method: 'PATCH',
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * @description Temp, to delete
	 *
	 * @tags Mining Result
	 * @name CreateResult
	 * @summary Create Result
	 * @request POST:/api/result/{job_id}
	 * @secure
	 */
	createResult = (jobId: string, data: ResultCreate, params: RequestParams = {}) =>
		this.http.request<
			KeywordRead | NamedEntityRead | (KeywordRead & NamedEntityRead),
			HTTPValidationError
		>({
			path: `/api/result/${jobId}`,
			method: 'POST',
			body: data,
			secure: true,
			type: ContentType.Json,
			format: 'json',
			...params
		});
	/**
	 * No description
	 *
	 * @tags Mining Result
	 * @name ReadResult
	 * @summary Read Result
	 * @request GET:/api/result/{result_id}
	 * @secure
	 */
	readResult = (resultId: string, params: RequestParams = {}) =>
		this.http.request<
			KeywordRead | NamedEntityRead | (KeywordRead & NamedEntityRead),
			HTTPValidationError
		>({
			path: `/api/result/${resultId}`,
			method: 'GET',
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * No description
	 *
	 * @tags Mining Result
	 * @name ListResultsForItem
	 * @summary List Results For Item
	 * @request GET:/api/result/list/{item_id}
	 * @secure
	 */
	listResultsForItem = (itemId: string, params: RequestParams = {}) =>
		this.http.request<
			(KeywordRead | NamedEntityRead | (KeywordRead & NamedEntityRead))[],
			HTTPValidationError
		>({
			path: `/api/result/list/${itemId}`,
			method: 'GET',
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * No description
	 *
	 * @tags Research Quality Snapshot
	 * @name CreateSnapshot
	 * @summary Create Snapshot
	 * @request POST:/api/snapshot/{item_id}/{case_id}
	 * @secure
	 */
	createSnapshot = (itemId: string, caseId: string, params: RequestParams = {}) =>
		this.http.request<SnapshotRead, HTTPValidationError>({
			path: `/api/snapshot/${itemId}/${caseId}`,
			method: 'POST',
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * No description
	 *
	 * @tags Research Quality Snapshot
	 * @name ReadResearchQualitySnapshot
	 * @summary Read Research Quality Snapshot
	 * @request GET:/api/snapshot/{snapshot_id}
	 * @secure
	 */
	readResearchQualitySnapshot = (snapshotId: string, params: RequestParams = {}) =>
		this.http.request<SnapshotRead, HTTPValidationError>({
			path: `/api/snapshot/${snapshotId}`,
			method: 'GET',
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * @description List snapshots for item, newest first
	 *
	 * @tags Research Quality Snapshot
	 * @name ListSnapshotsForItem
	 * @summary List Snapshots For Item
	 * @request GET:/api/snapshot/list/{item_id}
	 * @secure
	 */
	listSnapshotsForItem = (itemId: string, params: RequestParams = {}) =>
		this.http.request<SnapshotRead[], HTTPValidationError>({
			path: `/api/snapshot/list/${itemId}`,
			method: 'GET',
			secure: true,
			format: 'json',
			...params
		});
	/**
	 * @description Import an excel collection as provided by FESAD to the database and return the created documents. Note: * `services` is applied to **all** imported texts * One `Job` (with status `DRAFT`) for every `service`is created. * `DRAFT` means that it is excluded from being run * [cf. here](/docs#/Mining%20Job/start_job_api_job__job_id__start_patch) to start the job * If you want to use the created documents in a case, you'll need to create one separately and attach the returned documents there.
	 *
	 * @tags Task
	 * @name ImportDocumentsWithTextsFromFesadExcelCollection
	 * @summary Import Documents With Texts From Fesad Excel Collection
	 * @request POST:/api/task/fesad/excel_collection
	 * @secure
	 */
	importDocumentsWithTextsFromFesadExcelCollection = (
		data: BodyImportDocumentsWithTextsFromFesadExcelCollectionApiTaskFesadExcelCollectionPost,
		query?: { services?: TextWorkflow[] },
		params: RequestParams = {}
	) =>
		this.http.request<DocumentRead[], HTTPValidationError>({
			path: `/api/task/fesad/excel_collection`,
			method: 'POST',
			query: query,
			body: data,
			secure: true,
			type: ContentType.FormData,
			format: 'json',
			...params
		});
	/**
	 * @description Delete Cookie
	 *
	 * @tags Authenticate
	 * @name Logout
	 * @summary Logout
	 * @request POST:/api/auth/logout
	 */
	logout = (params: RequestParams = {}) =>
		this.http.request<any, any>({
			path: `/api/auth/logout`,
			method: 'POST',
			format: 'json',
			...params
		});
	/**
	 * @description Get access cookie Note: Your email is your `username`
	 *
	 * @tags Authenticate
	 * @name Login
	 * @summary Login
	 * @request POST:/api/auth/login
	 */
	login = (data: BodyLoginApiAuthLoginPost, params: RequestParams = {}) =>
		this.http.request<UserRead, HTTPValidationError>({
			path: `/api/auth/login`,
			method: 'POST',
			body: data,
			type: ContentType.UrlEncoded,
			format: 'json',
			...params
		});
}
