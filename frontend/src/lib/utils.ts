import * as yup from 'yup';
import { Buffer } from 'buffer/'; //cf. https://github.com/vitejs/vite/discussions/2785

export const focusElement = (idToFocus) => {
	const ele = document.querySelector(`#${idToFocus}`);
	if (ele) {
		// @ts-ignore
		ele.focus();
	}
};

const schema = yup.object().shape({
	uuid: yup.string().uuid()
});

export const isValidUUID = (value) => schema.isValidSync({ uuid: value });

export const getShortIfNeeded = (string, maxlength = 10) =>
	`${string.slice(0, maxlength).trim()}${string.length > maxlength ? '...' : ''}`;

export const makeDataURL = (value: any[]) => {
	const toExport = JSON.stringify(value);
	const encoded = Buffer.from(toExport).toString('base64');
	return `data:application/json;base64,${encoded}`;
};
