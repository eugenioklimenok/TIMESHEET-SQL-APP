from pydantic import BaseModel
from typing import Optional

class BaseResponse(BaseModel):
    status: Optional[str] = "OK"
    detail: Optional[str] = "La petición se ha ejecutado correctamente"
    error: Optional[str] = None