from fastapi import APIRouter, Depends, Request, Response
from app.models import subjects
from sqlalchemy.orm import Session
from app.db.connection import database
from app.schemas.keyword import KeywordList
from app.models import words
from app.response_schemas.keyword import KeywordListResult
import json

router = APIRouter(prefix="/api/keyword", tags=["키워드"])


@router.get("/list", description="키워드 리스트", response_model=list[KeywordListResult])
async def list(id: int, response: Response,
               db: Session = Depends(database)):
    wordlist = words.word_choice_list(db, id)
    return wordlist
