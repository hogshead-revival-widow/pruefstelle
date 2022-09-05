import { tick } from 'svelte';

export const closeModal = ({ id }: { id: string }) => {
	const toClose = document.querySelector(`input[type="checkbox"]#${id}`);
	if (!toClose) {
		throw new Error(`Modal mit ID ${id} nicht gefunden.`);
	}
	// @ts-ignore
	// The model is displayed via CSS, if its corresponding checkbox is checked
	toClose.checked = false;
};

const show = (id: string) => {
	// callback
	const toShow = document.querySelector(`input[type="checkbox"]#${id}`);
	if (!toShow) {
		throw new Error(`Modal mit ID ${id} nicht gefunden.`);
	}
	// @ts-ignore
	// The model is displayed via CSS, if its corresponding checkbox is checked
	toShow.checked = true;
};

export const showModal = ({ id }: { id: string }) => {
	/*
	A model may be added programmatically. Before showing it, we await the next tick,
	because an update is not rendered immediatly, i.e. the modal is not available before the next tick.
	*/
	tick().then(() => show(id));
};
