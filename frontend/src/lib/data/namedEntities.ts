import { NamedEntityType } from '$lib/api';

export const NAMED_ENTITY_TO_WORD = {
	[NamedEntityType.LOCATION]: 'Ort',
	[NamedEntityType.ORGANIZATION]: 'Organisation',
	[NamedEntityType.PERSON]: 'Person'
};

export const NAMED_ENTITY_TO_WORD_WITH_ARTICLE = {
	[NamedEntityType.LOCATION]: 'ein ' + NAMED_ENTITY_TO_WORD[NamedEntityType.LOCATION],
	[NamedEntityType.ORGANIZATION]: 'eine ' + NAMED_ENTITY_TO_WORD[NamedEntityType.ORGANIZATION],
	[NamedEntityType.PERSON]: 'eine ' + NAMED_ENTITY_TO_WORD[NamedEntityType.PERSON]
};
