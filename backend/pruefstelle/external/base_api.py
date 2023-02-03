from typing import Callable, Dict, TypeVar, Optional
from typing_extensions import ParamSpec

import requests
from requests.models import PreparedRequest
from pydantic import ValidationError, AnyHttpUrl

from .errors import ApiRequestError, ApiResponseError, ApiError


ReturnType = TypeVar("ReturnType")
ParamTypes = ParamSpec("ParamTypes")
PathsType = TypeVar("PathsType")


class Api:
    def __init__(
        self,
        base_url: str,
        header: Dict[str, str] = dict(
            Content_Type="application/json", Accept="application/json"
        ),
    ):
        self.url_scheme = "http" if base_url.startswith("http") else "https"
        self.base_url = base_url
        self.header = header
        self.verify = False

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
                except (
                    requests.exceptions.HTTPError,
                    requests.exceptions.ConnectionError,
                    requests.exceptions.RequestException,
                ) as request_error:
                    """The HTTP request erroed out / there was a network problem
                    or any other request related exception has occured"""
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
        base_url: Optional[str] = None,
    ) -> AnyHttpUrl:
        """Generate URL form `path`, including query parameters (`params`)"""
        if base_url is None:
            base_url = self.base_url
        url = base_url + path
        if params is not None:
            prepared_request = PreparedRequest()
            prepared_request.prepare_url(url, params)
            url = prepared_request.url
            if url is None:
                raise ApiError("Path -> URL failed while adding params (URL is `None`)")
        scheme = "http" if base_url.startswith("http") else "https"
        return AnyHttpUrl(url, scheme=scheme)
