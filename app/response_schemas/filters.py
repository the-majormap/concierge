from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional


class FilterEnum(str, Enum):
    WORD = "word"
    SUBJECT = "subject"


class FilterInputList(BaseModel):
    type: FilterEnum = Field(title="word,subject", default="subject")
    id: int
    score: int
