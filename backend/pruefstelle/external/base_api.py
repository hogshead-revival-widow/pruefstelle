from typing import Callable, Dict, TypeVar, Optional, Literal
from typing_extensions import ParamSpec

import requests
from requests.models import PreparedRequest
from pydantic import ValidationError, AnyHttpUrl, Json

from .errors import ApiRequestError, ApiResponseError, ApiError


OriginalReturn = TypeVar("OriginalReturn")
OriginalParams = ParamSpec("OriginalParams")

Header = Dict[str, str]


class Api:
    def __init__(
        self,
        url_scheme: Literal["http", "https"],
        base_url: str,
        header: Header = dict(
            Content_Type="application/json", Accept="application/json"
        ),
    ):
        self.url_scheme = url_scheme
        self.base_url = base_url
        self.header = header

    class ErrorHandling:
        """Error handling decorators"""

        @staticmethod
        def on_request_error(
            method: Callable[OriginalParams, OriginalReturn]
        ) -> Callable[OriginalParams, OriginalReturn]:
            """Handle errors on calls made by `Api`.
            (Currently only request exceptions in `ApiRequestError`.)
            """

            def handler(
                *args: OriginalParams.args, **kwargs: OriginalParams.kwargs
            ) -> OriginalReturn:
                try:
                    return method(*args, **kwargs)
                except (
                    requests.exceptions.HTTPError,
                    requests.exceptions.ConnectionError,
                    requests.exceptions.RequestException,
                ) as e:
                    """The HTTP request has any error status,
                    there was a network problem (e.g. DNS failure, refused connection)
                    or any other request related exception has occured."""
                    error = ApiRequestError(e)
                    error.response = e.response
                    raise error

            return handler

        @staticmethod
        def on_response_error(
            method: Callable[OriginalParams, OriginalReturn]
        ) -> Callable[OriginalParams, OriginalReturn]:
            """Handle errors regarding the response of `Api` calls.
            (Wrapping pydantic.ValidationError)
            """

            def handler(
                *args: OriginalParams.args, **kwargs: OriginalParams.kwargs
            ) -> OriginalReturn:
                try:
                    return method(*args, **kwargs)
                except ValidationError as validation_error:
                    """The response doesn't conform to the model"""
                    raise ApiResponseError(validation_error)

            return handler

    @ErrorHandling.on_request_error
    def _get(self, url: AnyHttpUrl) -> requests.Response:
        """Make a `GET` request"""
        response = requests.get(url, headers=self.header)
        response.raise_for_status()
        return response

    @ErrorHandling.on_request_error
    def _post(self, url: AnyHttpUrl, data: Json):
        """
        Make a `POST` request.

        Note: `data` is assumed to be a JSON encoded string
        """

        response = requests.post(url, data=data, headers=self.header)
        response.raise_for_status()
        return response

    def _path_to_url(
        self,
        path: str,
        params: Optional[Dict[str, str]] = None,
    ) -> AnyHttpUrl:
        """Generate URL form `path`, including query parameters (`params`)"""
        url = self.base_url + path
        if params is not None:
            prepared_request = PreparedRequest()
            prepared_request.prepare_url(url, params)
            url = prepared_request.url
            if url is None:
                raise ApiError("Path -> URL failed while adding params (URL is `None`)")
        return AnyHttpUrl(url, scheme=self.url_scheme)
