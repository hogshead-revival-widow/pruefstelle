/*
	Holds data for breadcrumbs.
	Note: The `page` argument expects the value of $app/store:$page
*/
import { get as $ } from 'svelte/store';
import { user } from '$lib/stores';
import { isValidUUID } from '$lib/utils';

export const withContext = (page, isDocument) => {
	return {
		label: isDocument === true ? 'Dokument in Fall' : 'Text in Fall',
		link: page.url.pathname
	};
};

export const enrichContext = (page, crumbs) => {
	if (
		page.url.pathname.includes('context') &&
		(page.url.pathname.includes('text') || page.url.pathname.includes('document')) &&
		page.url.pathname.split('/').length > 5 &&
		isValidUUID(page.url.pathname.split('/')[3]) &&
		isValidUUID(page.url.pathname.split('/')[5])
	) {
		crumbs = [...crumbs, withContext(page, page.url.pathname.includes('document'))];
	}

	return crumbs;
};

export const matchPage = (page) => [
	{
		label: 'Übersicht',
		icon: 'home',
		getLink: () => '/dashboard',
		match: 'dashboard',
		matched: false
	},
	{
		label: 'Dokument',
		match: (value) =>
			page.url.pathname.includes('/document') && page.url.pathname.includes('/evaluated'),
		getLink: () =>
			`/dashboard/document/${page.url.pathname.split('/').find((path) => isValidUUID(path))}`,
		matched: false
	},
	{
		label: 'Fall',
		match: (value) =>
			page.url.pathname.includes('/case') && page.url.pathname.includes('/evaluated'),
		getLink: () =>
			`/dashboard/case/${page.url.pathname.split('/').find((path) => isValidUUID(path))}`,
		matched: false
	},
	{
		label: 'Text',
		match: (value) =>
			page.url.pathname.includes('/text') && page.url.pathname.includes('/evaluated'),
		getLink: () =>
			`/dashboard/text/${page.url.pathname.split('/').find((path) => isValidUUID(path))}`,
		matched: false
	},
	{
		label: 'Fall hinzufügen',
		getLink: () => page.url.pathname,
		match: 'new',
		matched: false
	},

	{
		label: 'Text',
		match: (value) =>
			!page.url.pathname.includes('/evaluated') &&
			isValidUUID(value) &&
			page.url.pathname.includes('/text'),

		getLink: () =>
			page.url.pathname.includes('context')
				? page.url.pathname.split('/').splice(0, 4).join('/')
				: page.url.pathname,
		matched: false
	},
	{
		label: 'Dokument',
		match: (value) =>
			isValidUUID(value) &&
			page.url.pathname.includes('/document') &&
			!page.url.pathname.includes('/evaluated'),
		getLink: () =>
			page.url.pathname.includes('context')
				? page.url.pathname.split('/').splice(0, 4).join('/')
				: page.url.pathname,
		matched: false
	},
	{
		label: `Bezugsfall`,
		match: (value) => isValidUUID(value) && page.url.pathname.includes('/context'),
		getLink: () => `/dashboard/case/${page.url.pathname.split('/')[5]}`,
		matched: false
	},
	{
		label: 'Alle Fälle',
		getLink: () => '/dashboard/case',
		match: (value) =>
			page.url.pathname.includes('case') && !page.url.pathname.includes('/evaluated'),
		matched: false
	},
	{
		label: 'Fall',
		match: (value) =>
			page.url.pathname.includes('/case') &&
			isValidUUID(value) &&
			!page.url.pathname.includes('/evaluated'),
		getLink: () => page.url.pathname,
		matched: false
	},
	{
		label: $(user).email,
		getLink: () => '/dashboard/user',
		match: 'user',
		matched: false
	},
	{
		label: 'Meine Fälle',
		getLink: () => '/dashboard/user/has/onwatch',
		match: 'onwatch',
		matched: false
	},
	{
		label: 'Meine Bewertungen',
		getLink: () => page.url.pathname,
		match: (value) => value == 'evaluated',
		matched: false
	},
	{
		label: 'Meine E-Mail ändern',
		getLink: () => '/dashboard/user/mail',
		match: 'mail',
		matched: false
	},
	{
		label: 'Mein Passwort ändern',
		getLink: () => '/dashboard/user/password',
		match: 'password',
		matched: false
	}
];
