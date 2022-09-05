import { get as $ } from 'svelte/store';
import { Pruefstelle, type ps } from '$lib/api';
import { user, DefaultUser } from '$lib/stores/user';

export const handleLogout = async () => {
	await Pruefstelle.logout();
};
export const handleLogin = async (
	{ email, password },
	{ on401Error = () => {}, onOtherError = () => {}, onLoggedIn = () => {} }
) => {
	try {
		const data = { username: email, password: password };
		// If successfull, a cookie is set by the server storing the credentials
		const userRead = await Pruefstelle.login(data);
		user.set(userRead);
		onLoggedIn();
	} catch (error) {
		if (error.status == 401) {
			on401Error();
		} else {
			onOtherError();
		}
	}
};

// helper to access stores in load() functions, where direct store access is not possible
export const setUser = (readUser: ps.UserRead) => user.set(readUser);
export const resetUser = () => user.set(DefaultUser());

// True if user is stored; proper auth is handled by server-set cookie
const isKnown = () => {
	const isKnown = 'id' in $(user) && $(user).id !== undefined;
	if (isKnown === true) {
		return true;
	}
};

// The cookie may still be valid and the user could be treated as if he was logged in automatically
const getUserIfPossible = async () => {
	const userRead = await Pruefstelle.readSelf();
	return userRead;
};

export const isLoggedIn = async (storeUser = true) => {
	const userIsKnown = await isKnown();
	if (userIsKnown === true) return true;

	try {
		const readUser = await Pruefstelle.readSelf();
		if (storeUser) setUser(readUser);
		return true;
	} catch (error) {
		return false;
	}
};
