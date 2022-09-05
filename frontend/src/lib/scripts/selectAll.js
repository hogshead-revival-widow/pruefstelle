/*
	Handle "select all checkboxes" and save selection to store
*/
import { writable, get as $ } from 'svelte/store';

export const watchSelected = ({ idAll, selectionItems, prefix }) => {
	/*
		Args:
			* id-all: id of the "check all" checkbox, not including the prefix
		    * selectionItems: [itemWithUniqueIDProperty,...];
			* prefix: prefix of all checkboxes as used in the input attribute `id`

			* Example:
				* Args: {id-all: "all", selectionItems: thisDocument.texts, prefix: `select-text-${thisDocument.id}`}
			    * IDs:
					* <checkbox all>: select-text-${thisDocument.id}-all
					* <checbkox item>: select-text-${thisDocument.id}-{thisText.id}
		Returns:
			* Object with properties:
				* `toggleSelect` (function, to be used in on:change for every checkbox except the "select all" checkbox),
			   	* `toggleSelectAll` (function, to be used in on:change for the "select all" checkbox)
				* `selected` (store, holding a `set` of  selected items)
			   	* `reset` (function, usable to reset the selection)
	*/
	let selected = writable(new Set());
	const identifiers = selectionItems === undefined ? [] : Array.from(selectionItems, (d) => d.id);
	const updateChecked = () => {
		identifiers
			.filter((id) => !(id in $(selected)))
			// @ts-ignore
			.forEach((id) => {
				const toCheck = document.querySelector(`input#${prefix}-${id}`);
				if (toCheck) {
					// @ts-ignore
					toCheck.checked = false;
				}
			});
		// @ts-ignore
		$(selected).forEach((id) => {
			const toCheck = document.querySelector(`input#${prefix}-${id}`);
			if (toCheck) {
				// @ts-ignore
				toCheck.checked = true;
			}
		});
		if ($(selected).size === identifiers.length) {
			// @ts-ignore
			const toCheck = document.querySelector(`input#${prefix}-${idAll}`);
			if (toCheck) {
				// @ts-ignore
				toCheck.checked = true;
			}
		} else {
			// @ts-ignore
			const toCheck = document.querySelector(`input#${prefix}-${idAll}`);
			if (toCheck) {
				// @ts-ignore
				toCheck.checked = false;
			}
		}
	};
	// @ts-ignore
	const toggleSelect = (event, value) => {
		if (event.target.checked) {
			$(selected).add(event.target.value);
			selected.set($(selected));
		} else {
			$(selected).delete(event.target.value);
			selected.set($(selected));
		}
		updateChecked();
	};
	const toggleSelectAll = (event) => {
		if (event.target.checked) {
			selected.set(new Set(identifiers));
		} else {
			selected.set(new Set());
		}

		updateChecked();
	};

	const setSelection = (ids) => {
		selected.set(new Set(ids));
		updateChecked();
	};
	const reset = () => {
		selected.set(new Set());
		updateChecked();
	};

	const getSelection = () => {
		return $(selected);
	};
	return {
		getSelection,
		toggleSelect,
		toggleSelectAll,
		selected, // this is a set stored in a store
		reset,
		setSelection
	};
};
