/* API base configuration */

import type { ApiConfig } from "./http-client";

export const configuration: ApiConfig = {
	// @ts-ignore
	baseUrl: import.meta.env.VITE_API_BASE_URL,
	baseApiParams: { credentials: 'include', mode: 'cors' }
};
