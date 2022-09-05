from ..errors import PruefstelleError


class TaskError(PruefstelleError):
    user_message: str = "Something unexpected happened while handling a task"


class JobError(TaskError):
    user_message: str = (
        "Something unexpected happened while handling a job-related task"
    )


class FesadError(TaskError):
    """
    Something unexpected happend while handling a fesad-related task
    """

    user_message: str = (
        "Something unexpected happened while handling a fesad-related task"
    )


class DUNotFoundError(FesadError):
    pass


class MissingNeeededCategoryError(FesadError):
    pass


class PointsError(TaskError):
    """
    Something unexpected happend during point calculation
    """

    user_message: str = "Something unexpected happened while calculating points, most likely due to wrong references (UUIDs)"


class PointsCalulationMissingInformation(PointsError):
    """
    Something unexpected happend during point calculation
    """

    user_message: str = "Some information is missing, most likely because not all items have been evaluated yet"
