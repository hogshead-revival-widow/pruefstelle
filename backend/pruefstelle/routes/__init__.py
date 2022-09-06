"""
For clarity, only the path security dependencies for the admin routes are declared here.
For all other routes, they are declared directly in the function signature of the route
"""
from fastapi import APIRouter
from ..security import AuthenticatedUser, AdminUser

from .category import router as category_router
from .case import router as case_router
from .document import router as document_router
from .user import router as user_router
from .text import router as text_router
from .job import router as job_router
from .result import router as result_router
from .evaluation import router as evaluation_router
from .snapshot import router as snapshot_router
from .report import router as report_router

from .tasks import router as task_router


from .admin import router as admin_router
from .security import router as security_router

# Change the order here to change the order displayed in docs
main_router = APIRouter(prefix="/api")

main_router.include_router(case_router, prefix="/case", tags=["Case"])

main_router.include_router(document_router, prefix="/document", tags=["Document"])
main_router.include_router(text_router, prefix="/text", tags=["Text"])
main_router.include_router(evaluation_router, prefix="/evaluation", tags=["Evaluation"])
main_router.include_router(report_router, prefix="/report", tags=["Report"])

main_router.include_router(category_router, prefix="/category", tags=["Category"])
main_router.include_router(user_router, prefix="/user", tags=["User"])

main_router.include_router(job_router, prefix="/job", tags=["Mining Job"])
main_router.include_router(result_router, prefix="/result", tags=["Mining Result"])

main_router.include_router(
    snapshot_router, prefix="/snapshot", tags=["Research Quality Snapshot"]
)
main_router.include_router(task_router, prefix="/task", tags=["Task"])


main_router.include_router(security_router, prefix="/auth", tags=["Authenticate"])
main_router.include_router(
    admin_router, prefix="/admin", tags=["Administration"], dependencies=[AdminUser]
)
