from fastapi import APIRouter, Depends, Request, Response
from app.models import subjects
from sqlalchemy.orm import Session
from app.db.connection import database
from app.schemas.subjects import SubjectList
from app.response_schemas.subjects import SubjectListResult
import json

router = APIRouter(prefix="/api/subjects", tags=["과목"])


@router.post("/list", description="과목 리스트", response_model=list[SubjectListResult])
async def list(subjectlist: SubjectList, response: Response,
               db: Session = Depends(database)):
    subject_list = subjects.subject_choice_list(db)
    return subject_list