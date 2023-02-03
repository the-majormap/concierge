from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from app.schemas.list_default import Pageing


class KeywordList(BaseModel):
    pageing: Pageing