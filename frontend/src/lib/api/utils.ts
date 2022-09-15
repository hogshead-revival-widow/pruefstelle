import type * as ps from '$lib/api/contracts';
import { Status } from '$lib/api/contracts';

export type CaseDocumentText =
	| ps.CaseRead
	| ps.DocumentRead
	| ps.DocumentReadWithoutCases
	| ps.TextRead;

// Differentiate item by type

export const isKeyword = (result: ps.AnyResult): result is ps.KeywordRead => {
	if ((result as ps.KeywordRead).keyword) return true;
	return false;
};

export const isTopic = (result: ps.AnyResult): result is ps.TopicRead => {
	if ((result as ps.TopicRead).given_topic_id) return true;
	return false;
};

export const isEntity = (result: ps.AnyResult): result is ps.NamedEntityRead => {
	if ((result as ps.NamedEntityRead).type) return true;
	return false;
};

export const isCase = (unknown: CaseDocumentText): unknown is ps.CaseRead => {
	if ((unknown as ps.CaseRead).watchers) return true;
	return false;
};

export const isDocument = (
	unknown: CaseDocumentText
): unknown is ps.DocumentRead | ps.DocumentReadWithoutCases => {
	if ((unknown as ps.DocumentRead).external_id) return true;
	return false;
};

export const isText = (unknown: CaseDocumentText): unknown is ps.TextRead => {
	if ((unknown as ps.TextRead).discriminator) return true;
	return false;
};

// Status

const jobHasError = (job: ps.JobRead, draftIsError: boolean = true) => {
	const currentStatus = job.status;
	const errorStatus = [Status.FAILED, Status.NON_API_ERROR, Status.PARTIALLY_COMPLETED];
	if (draftIsError) errorStatus.push(Status.DRAFT);
	return errorStatus.some((errorStatus) => errorStatus === currentStatus);
};

const jobIsFinished = (job: ps.JobRead) => {
	const currentStatus = job.status;
	const doneStatus = Status.RESULTS_IN_DB;
	return currentStatus === doneStatus;
};

const getJobs = (item: CaseDocumentText) => {
	if (isCase(item))
		return item.documents.flatMap((readDocument) =>
			readDocument.items.flatMap((item) => item.mining_jobs)
		);

	if (isDocument(item)) return item.items.flatMap((item) => item.mining_jobs);

	return item.mining_jobs;
};

export const hasError = (item: CaseDocumentText) => getJobs(item).some((job) => jobHasError(job));
export const hasFinished = (item: CaseDocumentText) =>
	getJobs(item).every((job) => jobIsFinished(job));

export const needsReload = (item: CaseDocumentText) => {
	const jobs = getJobs(item);
	// stop reloading if any job has an error
	// or not every job is finished
	const stopReloading =
		jobs.some((job) => jobHasError(job)) || jobs.every((job) => jobIsFinished(job));
	return !stopReloading;
};
