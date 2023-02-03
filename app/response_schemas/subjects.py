from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional
from app.schemas.list_default import Pageing


class SubjectCategoryEnum(str, Enum):
    RESEARCH = "탐구"
    CULTURE = "생활교양"
    BASIC = "기초"
    ART = "체육예술"
    SPECIALZED_1 = "전문교과Ⅰ"
    SPECIALZED_2 = "전문교과Ⅱ"


class SubjectSelectorEnum(str, Enum):
    MAJOR = "진로선택"
    COMMON = "공통"
    BASIC = "일반선택"


class SubjectListResult(BaseModel):
    id: int = Field(title="기본키", default=21)
    category: SubjectCategoryEnum = Field(title="카테고리")
    kind: str | None = Field(title="종류", default="수학")
    name: str = Field(title="과목명", default="경제 수학")
    prerequisites: str | None = Field(title="이전에 배워야 하는과목", default="수학Ⅰ")
    selector: SubjectSelectorEnum = Field(title="상위 카테고리")
