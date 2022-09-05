from typing import Optional, Any
from fastapi import HTTPException


def raise_404_for_None(value: Optional[Any], detail: Optional[str] = None):
    if value is None:
        info = "Item(s) not found, this is most likely due to a wrong reference (UUID)."
        if detail is None:
            detail = info
        else:
            detail = f"""{info}. More: {detail}"""

        raise HTTPException(status_code=404, detail=detail)


def raise_401_for_violation(must_be_true: bool, detail: Optional[str] = None):
    """
    Raise 401, if `must_be_true` is False
    """
    if must_be_true is False:
        if detail is None:
            detail = "Not authorized for this action"
        raise HTTPException(status_code=401, detail=detail)
