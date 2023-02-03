from fastapi import APIRouter, Depends, Request, Response
from app.models import subjects
from sqlalchemy.orm import Session
from app.db.connection import database
from app.schemas.keyword import KeywordList
from app.models import words, filters, majors
from app.response_schemas.keyword import KeywordListResult
import json

router = APIRouter(prefix="/api/major", tags=["추천"])


@router.post("/recommend", description="추천 리스트")
async def list(id: int, response: Response,
               db: Session = Depends(database)):
    fl = filters.filter_detail(db, id).first()
    return majors.major_recommend_list(db, fl.university_id, fl.id)

