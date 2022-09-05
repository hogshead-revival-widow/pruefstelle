/*
    Import api client from here.
    Note:
    - use `makePruefstelle` inside load() to pass svelte-patched `fetch`
    - use `Pruefstelle` in all other cases
*/

import { Api } from '$lib/api/Api';
import { HttpClient } from '$lib/api/http-client'
import { configuration } from '$lib/api/configuration';

interface IMakePruefstelle{ customFetch?: typeof fetch, customClient?: HttpClient }

const makeClient = (config = configuration) => new HttpClient(config);

// use this inside load
export const makePruefstelle = ({customFetch = undefined, customClient = makeClient(configuration) }: IMakePruefstelle = {}) => {
	const client = customClient

	if (customFetch !== undefined) {
		client.customFetch = (...params) => customFetch(...params);

	}

	return new Api(client);
}

// use this outside load
export const Pruefstelle = makePruefstelle({customFetch: undefined})
