from fastapi import Cookie, FastAPI, Request, Depends
from typing import Optional, List
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends
from app.models import filters
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from app.db.connection import database

router = APIRouter(prefix="/major", tags=["채팅"])
templates = Jinja2Templates(directory="templates")


@router.get("/list")
async def list(id: int, request: Request, db: Session = Depends(database)):
    fl = filters.filter_detail(db, id).first()

    return templates.TemplateResponse("major/list.html", {"request": request})
