import { goto } from '$app/navigation';

import { Pruefstelle, type ps } from '$lib/api';
import { addAlert } from './alerts';
import { user } from '$lib/stores';

export const updatePassword = async ({ currentPassword, password }) => {
	try {
		const data: ps.UserUpdate = {
			current_password: currentPassword,
			new_password: password
		};
		const userRead = await Pruefstelle.updateSelf(data);
		addAlert({ message: 'Passwort aktualisiert', type: 'success' });
		goto('/dashboard/');
	} catch (error) {
		if (error.status === 401) {
			addAlert({
				message: 'Konnte Passwort nicht ändern. Hast Du das bisherige Passwort angegeben?',
				type: 'error'
			});
		} else {
			addAlert({ message: 'Konnte Passwort nicht ändern.', type: 'error' });
		}
	}
};

export const updateEmail = async ({ password, email }) => {
	try {
		const data: ps.UserUpdate = {
			current_password: password,
			email: email
		};
		const userRead = await Pruefstelle.updateSelf(data);
		user.set(userRead);
		addAlert({ message: 'Email geändert!', type: 'success' });
		goto('/dashboard/');
	} catch (error) {
		let message = '';
		if (error.status === 401) {
			message = 'Konnte Email nicht ändern. Ist das Passwort korrekt?';
		} else {
			message =
				'Konnte Email nicht ändern.  Möglicherweise ist diese Adresse schon in Benutzung. Tipp: Versuche es mit einer anderen Email.';
		}

		addAlert({
			message,
			type: 'error'
		});
	}
};
