from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class Pageing(BaseModel):
    page: int
    limit: Optional[int] = 0