from fastapi import APIRouter
from .case import router as case_router
from .category import router as category_router
from .document import router as document_router
from .evaluation import router as evaluation_router
from .text import router as text_router
from .user import router as user_router

router = APIRouter()


router.include_router(case_router, prefix="/case")
router.include_router(category_router, prefix="/category")
router.include_router(document_router, prefix="/document")
router.include_router(evaluation_router, prefix="/evaluation")
router.include_router(text_router, prefix="/text")
router.include_router(user_router, prefix="/user")
