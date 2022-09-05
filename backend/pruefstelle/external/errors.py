from requests import Response

from ..errors import PruefstelleError


class ApiError(PruefstelleError):
    pass


class ApiRequestError(ApiError):
    response: Response


class ApiResponseError(ApiError):
    pass
