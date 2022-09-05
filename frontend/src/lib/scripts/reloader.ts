import { needsReload, type CaseDocumentText } from '$lib/api/utils';

export type RefreshState = () => Promise<CaseDocumentText>;

// to be used inside onMount()
export const reloader = async (item: CaseDocumentText, refreshState: RefreshState) => {
	if (!needsReload(item)) return;
	let intervalID = undefined;
	const reload = async () => {
		const item = await refreshState();
		if (!needsReload(item)) {
			clearInterval(intervalID);
		}
	};
	// @ts-ignore
	const pollingInterval = <number>import.meta.env.VITE_API_UPDATE_INTERVAL;
	intervalID = setInterval(reload, pollingInterval);

	// as reloader is a callback in onMount
	// the returned function will be called on destroy
	return () => clearInterval(intervalID);
};
