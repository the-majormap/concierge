from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from app.schemas.list_default import Pageing


class FilterRecord(BaseModel):
    filter_id: int
    word_id: Optional[int]
    subject_id: Optional[int]
    value: int

