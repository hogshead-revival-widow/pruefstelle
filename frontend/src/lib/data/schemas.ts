import * as yup from 'yup';

const title = yup.string().required('Bitte Titelnotiz angeben');
const category_id = yup
	.string()
	.required('Bitte Kategorie auswählen')
	.uuid('Bitte Kategorie auswählen');

const email = yup.string().required('Bitte Email angeben').email('Das ist keine Email');

export const addCaseSchema = yup.object().shape({ title, category_id });

export const addDocumentSchema = yup.object().shape({
	title,
	external_id: yup.string().required('Bitte Referenz angeben'),
	external_id_category_id: yup.string().required('Bitte Referenztyp wählen'),
	category_id
});

export const loginByLinkSchema = yup.object().shape({ email });

export const loginSchema = yup
	.object()
	.shape({ email, password: yup.string().required('Bitte Password angeben') });

export const getMailSchema = (currentMail) =>
	yup.object().shape({
		password: yup.string().required('Bitte Passwort angeben'),
		email: email.notOneOf([currentMail, null], 'Das ist bereits deine Email'),
		emailConfirm: email
			.notOneOf([currentMail, null], 'Das ist bereits deine Email')
			.oneOf([yup.ref('email'), null], 'Die Emails stimmen nicht überein')
	});

export const passwordSchema = yup.object().shape({
	currentPassword: yup.string().required('Bitte aktuelles Passwort angeben'),
	password: yup
		.string()
		.required('Bitte neues Passwort angeben')
		.notOneOf([yup.ref('currentPassword'), null], 'Das neue Passwort entspricht dem alten'),
	passwordConfirm: yup
		.string()
		.required('Bitte Passwort angeben')
		.oneOf([yup.ref('password'), null], 'Die Passwörter stimmen nicht überein')
		.notOneOf([yup.ref('currentPassword'), null], 'Das neue Passwort entspricht dem alten')
});
