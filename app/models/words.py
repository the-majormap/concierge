from typing import Optional
from sqlalchemy import Boolean, Date, Column, ForeignKey, BigInteger, DateTime, Integer, String, TIMESTAMP, Float, \
    FetchedValue, desc, update, select, \
    Text, distinct
from sqlalchemy.sql import text, func
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql.functions import count
from app.db.connection import database, Base
from starlette.exceptions import HTTPException
import datetime
from sqlalchemy.dialects.postgresql import JSONB


class Words(Base):
    __tablename__ = "words"
    id = Column(BigInteger, primary_key=True)
    wo_value = Column(String(50))
    embedding_vector = Column(JSONB)
    coord = Column(JSONB)


def word_choice_from():
    return """universities as u 
 	inner join 
 		majors as m 
 	on 
 		m.university_id=u.id
 	inner join
 		featured_majors as cm
 	on 
 		cm.major_id  = m.id
 	inner join 
 		featured_major_wordcloud_entities as cmwe 
 	on 
 		cmwe.featured_major_id = cm.id
 	inner join 
 		words as w 
 	on
 		w.id = cmwe.word_id
 	where u.id = :university_id	"""


def word_choice_count(db: Session, university_id, page=0, limit=10):
    query = """                
 select 
	count(distinct w.id)
 from """ + word_choice_from()
    stmt = text(query).bindparams(university_id=university_id)
    result = db.execute(stmt).all()
    return result


def word_choice_list(db: Session, university_id, page=0, limit=10):
    query = """
    select 
        id,
        keyword,
        score
    from                    
 (select 
    w.id,
	w.wo_value as keyword,
	sum(cmwe.fmwe_score) as score
 from """ + word_choice_from() + """
 group by 
 	w.id,
 	w.wo_value
 order by 
    sum(cmwe.fmwe_score) desc 	
 limit 500	
 	) as tab 
order by
 	score*random() desc"""
    if page > 0:
        query = query + " limit :limit offset :offset"
        stmt = text(query).bindparams(university_id=university_id, limit=limit, offset=((page - 1) * limit))
    else:
        stmt = text(query).bindparams(university_id=university_id)
    result = db.execute(stmt).all()
    return result
