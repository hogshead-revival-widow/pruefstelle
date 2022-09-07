from typing import Callable, Dict, TypeVar, Optional, Literal
from typing_extensions import ParamSpec

import requests
from requests.models import PreparedRequest
from pydantic import ValidationError, AnyHttpUrl

from .errors import ApiRequestError, ApiResponseError, ApiError


ReturnType = TypeVar("ReturnType")
ParamTypes = ParamSpec("ParamTypes")
PathsType = TypeVar("PathsType")

Header = Dict[str, str]


class Api:
    def __init__(
        self,
        url_scheme: Literal["http", "https"],
        base_url: str,
        header: Header = dict(
            Content_Type="application/json", Accept="application/json"
        ),
        verify=None,
    ):
        self.url_scheme = url_scheme
        self.base_url = base_url
        self.header = header
        self.verify = verify

    class ErrorHandling:
        """Hold decorators for Api"""

        @staticmethod
        def on_request_error(
            method: Callable[ParamTypes, ReturnType]
        ) -> Callable[ParamTypes, ReturnType]:
            """Handle errors on calls made by `Api`.
            Note: Wraps currently only request exceptions in `ApiRequestError`.
            """

            def handler(
                *args: ParamTypes.args, **kwargs: ParamTypes.kwargs
            ) -> ReturnType:
                try:
                    return method(*args, **kwargs)
                except requests.exceptions.HTTPError as http_error:
                    """The HTTP request has any error status"""
                    error = ApiRequestError(http_error)  # type: ignore
                    error.response = http_error.response
                    raise error
                except requests.exceptions.ConnectionError as connection_error:
                    """There is a network problem (e.g. DNS failure, refused connection)"""
                    error = ApiRequestError(connection_error)  # type: ignore
                    error.response = connection_error.response
                    raise error
                except requests.exceptions.RequestException as request_error:
                    """Any other request related exception has occured"""
                    error = ApiRequestError(request_error)  # type: ignore
                    error.response = request_error.response
                    raise error

            return handler

        @staticmethod
        def on_response_error(
            method: Callable[ParamTypes, ReturnType]
        ) -> Callable[ParamTypes, ReturnType]:
            """Handle errors regarding the response of `Api` calls.
            Note: Currently just wrapping  `pydantic:ValidationError` in `ApiResponseError`.
            """

            def handler(
                *args: ParamTypes.args, **kwargs: ParamTypes.kwargs
            ) -> ReturnType:
                try:
                    return method(*args, **kwargs)
                except ValidationError as validation_error:
                    """The response doesn't conform to the model"""
                    raise ApiResponseError(validation_error)  # type: ignore

            return handler

    @ErrorHandling.on_request_error
    def _get(self, url: AnyHttpUrl) -> requests.Response:
        """Make a `GET` request"""
        if self.verify is None:
            response = requests.get(url, headers=self.header)
        else:
            response = requests.get(url, headers=self.header, verify=self.verify)
        response.raise_for_status()
        return response

    @ErrorHandling.on_request_error
    def _post(self, url: AnyHttpUrl, data: str):
        """
        Make a `POST` request.

        Note: `data` is assumed to be a JSON encoded string
        """
        if self.verify is None:
            response = requests.post(url, data=data, headers=self.header)
        else:
            response = requests.post(
                url, data=data, headers=self.header, verify=self.verify
            )
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
