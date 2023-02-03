from typing import Optional
from sqlalchemy import Boolean, Date, Column, ForeignKey, BigInteger, DateTime, Integer, String, TIMESTAMP, \
    FetchedValue, desc, update, select, \
    Text, distinct, Float
from sqlalchemy.sql import text, func
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql.functions import count
from app.db.connection import database, Base
from starlette.exceptions import HTTPException
import datetime
from sqlalchemy.dialects.postgresql import JSONB


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(BigInteger, primary_key=True)
    category = Column(String(20))
    kind = Column(String(20))
    selector = Column(String(20))
    name = Column(String(50))
    prerequisites = Column(String(50))
    summary = Column(Text)
    related_jobs = Column(String(200))
    related_majors = Column(String(200))
    extras = Column(JSONB)
    description = Column(Text)
    embedding_vector = Column(JSONB)
    coord = Column(JSONB)


class Subject_wordcloud_entities(Base):
    __tablename__ = 'subject_wordcloud_entities'
    id = Column(BigInteger, primary_key=True)
    swe_score = Column(Float)
    subject_id = Column(BigInteger)
    word_id = Column(BigInteger)


def subject_choice_count(db: Session):
    query = """
    SELECT 
        count(s.id) as cnt          
    FROM subjects as s
           """
    stmt = text(query)
    result = db.execute(stmt).all()
    return result


def subject_choice_list(db: Session):
    query = """
select 
    s.id,
    s.category,
    s.kind,
    s.name,
    s.prerequisites,
    s.selector  
from subjects as s
       """
    stmt = text(query)
    result = db.execute(stmt).all()
    return result
