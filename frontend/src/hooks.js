export const handle = async ({ event, resolve }) => {
	/* ssr: false disables ssr in development, too */
	const response = await resolve(event, { ssr: false });

	return response;
};
