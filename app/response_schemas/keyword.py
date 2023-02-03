from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional
from app.schemas.list_default import Pageing


class KeywordListResult(BaseModel):
    id: int = Field(title="기본키", default=21)
    keyword: str = Field(title="키워드", default="교육")
    score: float = Field(title="점수(랜덤)", default=7.480109363794327)
