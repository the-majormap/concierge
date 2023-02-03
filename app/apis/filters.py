from fastapi import APIRouter, Depends, Request, Response
from app.models import subjects
from sqlalchemy.orm import Session
from app.db.connection import database
from app.schemas.keyword import KeywordList
from app.models import words, filters
from app.response_schemas.filters import FilterInputList
from app.schemas.filters import FilterRecord as FilterRecordSchema
import json

router = APIRouter(prefix="/api/filters", tags=["필터"])


@router.post("/input", description="임시 저장")
async def input(inputlist: list[FilterInputList], request: Request, response: Response,
                db: Session = Depends(database)):
    filter_id = filters.add_filter(db, request.client.host)
    for filterList in inputlist:
        input = FilterRecordSchema
        input.filter_id = filter_id
        input.value = filterList.score
        if filterList.type == "word":
            input.word_id = filterList.id
            input.subject_id = 0
        else:
            input.word_id = 0
            input.subject_id = filterList.id
        filters.add_filter_record(db, input)
    return filter_id

