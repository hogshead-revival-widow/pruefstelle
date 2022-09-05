import { writable, type Writable, get as $, get } from 'svelte/store';

export type AlertType = 'info' | 'error' | 'success' | 'warning';
type AlertObject = { id: number; message: string; type: AlertType };

// Hold all alerts; access via addAlert() / removeAlert()
export const alerts: Writable<AlertObject[]> = writable([]);

export const addAlert = ({ message, type = 'info' }: { message: string; type?: AlertType }) => {
	// Add alert
	const id = $(alerts).length > 0 ? $(alerts)[0].id + 1 : 0;
	const newAlert = { id, message, type };
	const updatedAlerts = [newAlert, ...$(alerts)];
	alerts.set(updatedAlerts);
	return id;
};

export const removeAlert = ({ id }: { id: number }) => {
	// Remove alert
	alerts.set($(alerts).filter((alert) => alert.id !== id));
};
