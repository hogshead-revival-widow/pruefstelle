import { TextWorkflow } from '$lib/api';

export const DEFAULT_WORKFLOWS = {
	[TextWorkflow.KeywordExtraction]: true,
	[TextWorkflow.NamedEntityRecognition]: true,
	[TextWorkflow.TopicModeling]: true
};

export const WORKFLOW_TO_WORD = {
	[TextWorkflow.KeywordExtraction]: 'Keyword-Extraction',
	[TextWorkflow.NamedEntityRecognition]: 'Named-Entity-Recognition',
	[TextWorkflow.TopicModeling]: 'Topic-Modeling'
};
