from typing import Annotated

from fastapi import Depends


async def get_db() -> None:
    """Replace with actual database dependency if needed."""
    return None


DBDependency = Annotated[None, Depends(get_db)]
