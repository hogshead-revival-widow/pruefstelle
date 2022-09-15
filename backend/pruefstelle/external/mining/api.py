from typing import Union
from uuid import UUID


from pydantic import BaseModel

from ..base_api import Api
from ...config import settings
from .schemas import (
    TextOrder,
    TextOrderParams,
    TextWorkflow,
    OrderReceipt,
    OrderStatus,
    ResultKeywords,
    ResultNamedEntities,
    ResultTopics,
)


class MiningApi(Api):
    class Paths(BaseModel):
        """Paths to endpoints"""

        base_url: str = settings.MINING_SERVICE.BASE_URL  # type: ignore
        new = "/orders/{workflow}"
        status = "/orders/{order_id}"
        result_keywords = "/orders/{order_id}/keywords"
        result_named_entities = "/orders/{order_id}/named-entities"
        result_linked_entities = "/orders/{order_id}/linked_entities"
        result_topics = "/orders/{order_id}/topics"

    def __init__(self):
        self.paths = MiningApi.Paths()
        super().__init__(base_url=self.paths.base_url)

    @Api.ErrorHandling.on_response_error
    def new_text_order(
        self,
        workflow: TextWorkflow,
        order: TextOrder,
        order_query_params: TextOrderParams = TextOrderParams(),
    ) -> OrderReceipt:
        """Create new mining order"""

        params = dict(order_query_params)
        path = self.paths.new.format(workflow=workflow)
        url = self._path_to_url(path=path, params=params)
        data = order.json()
        response = self._post(url, data)
        data = response.json()
        return OrderReceipt(**data)

    @Api.ErrorHandling.on_response_error
    def get_status(self, order_id: UUID) -> OrderStatus:
        """Get status of job identified by `order_id`"""
        path = self.paths.status.format(order_id=order_id)
        url = self._path_to_url(path=path)
        response = self._get(url)
        data = response.json()
        # if "keywords" in data:
        #    for index, keyword in enumerate(keyword):
        #        data["keywords"][index]["relevance"] = data["keywords"][index]["relevance"][:9]
        return OrderStatus(**data)

    @Api.ErrorHandling.on_response_error
    def get_text_result(
        self,
        order_id: UUID,
        workflow: TextWorkflow,
    ) -> Union[ResultKeywords, ResultNamedEntities]:
        """Get result of job identified by `order_id`"""

        # All workflows in `TextWorkflows` need to mapped
        workflow_to_text_result = {
            TextWorkflow.KEYWORD_EXTRACTION: {
                "path": self.paths.result_keywords,
                "result": ResultKeywords,
            },
            TextWorkflow.NAMED_ENTITY_RECOGNITION: {
                "path": self.paths.result_named_entities,
                "result": ResultNamedEntities,
            },
            TextWorkflow.TOPIC: {
                "path": self.paths.result_topics,
                "result": ResultTopics,
            },
            # TextWorkflow.NAMED_ENTITY_LINKING: {
            #    "path": self.paths.result_linked_entities,
            #    "result": ResultNamedEntities,
            # },
        }

        path = workflow_to_text_result[workflow]["path"]
        path = path.format(order_id=order_id)
        url = self._path_to_url(path)

        response = self._get(url)
        data = response.json()
        result = workflow_to_text_result[workflow]["result"]
        if workflow == TextWorkflow.NAMED_ENTITY_RECOGNITION:
            # the mining api returns a `text` property,
            # but NamedEntity has a `text` attribute referencing its text
            for index, _ in enumerate(data["named_entities"]):
                data["named_entities"][index]["label"] = data["named_entities"][index][
                    "text"
                ]
                data["named_entities"][index].pop("text")
        if "keywords" in data:
            for index, keyword in enumerate(data["keywords"]):
                data["keywords"][index]["relevance"] = "{:.2f}".format(
                    float(data["keywords"][index]["relevance"])
                )
        return result(order_id=order_id, **data)
