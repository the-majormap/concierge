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
from app.schemas.filters import FilterRecord as FilterRecordSchema


class FilterRecord(Base):
    __tablename__ = "filter_record"
    id = Column(BigInteger, primary_key=True)
    fr_ip_address = Column(String)
    university_id= Column(Integer)
    fr_creation_time = Column(DateTime(timezone=True), server_default=func.utcnow())


class FilterRecordRegster(Base):
    __tablename__ = "filter_record_regster"
    id = Column(BigInteger, primary_key=True)
    filter_id = Column(BigInteger)
    word_id = Column(BigInteger)
    fr_value = Column(Integer)
    subject_id = Column(BigInteger)


def add_filter(db: Session, ip: str):
    filter = FilterRecord(fr_ip_address=ip)
    db.add(filter)
    db.commit()
    db.refresh(filter)
    return filter.id


def add_filter_record(db: Session, schema: FilterRecordSchema):
    if schema.subject_id > 0:
        filter = FilterRecordRegster(filter_id=schema.filter_id, fr_value=schema.value,
                                     subject_id=schema.subject_id)
    else:
        filter = FilterRecordRegster(filter_id=schema.filter_id, fr_value=schema.value,
                                     word_id=schema.word_id)
    db.add(filter)
    db.commit()
    db.refresh(filter)
    return filter


def filter_detail(db: Session, id: int):
    result = db.query(FilterRecord).filter(FilterRecord.id == id)
    return result



def filter_record_list(db: Session, university_id=0, filter_id=10):
    query = """
select 
	sum(score),
	tab.featured_major_id,
	tab.ma_name,
	tab.major_id,
	m2.university_id 
from (select 	
        case when cmwe.fmwe_score > 0 then cmwe.fmwe_score*(frr.fr_value/100::float) else swe.fmse_score *(frr.fr_value/100::float) end as score,
        frr.fr_value,
        frr.id,
        case when swe.featured_major_id  is null then cmwe.featured_major_id  else swe.featured_major_id end as featured_major_id,
        case when swe.ma_name  is null then cmwe.ma_name  else swe.ma_name end as ma_name,
        case when swe.major_id  is null then cmwe.major_id  else swe.major_id end as major_id
    from 
        filter_record as fr
    inner join 
        filter_record_regster as frr 
    on
        fr.id = frr.filter_id
    left join (
        select 
            fmse.id,
            fmse.fmse_score,
            fmse.subject_id,
            fmse.featured_major_id,
            m.ma_name,
            m.id as major_id
        from 
            filter_record as fr
        inner join 
            filter_record_regster as frr 
        on
            fr.id = frr.filter_id	
        inner join 	
            featured_major_subjectcloud_entities as fmse 
        on
            frr.subject_id = fmse.subject_id 
        inner join 
            featured_majors as fm 
        on 
            fm.id = fmse.featured_major_id
        inner join 
            majors as m 
        on 
            m.id = fm.major_id 
        where 	
            m.university_id = :university_id
        ) as swe 
    on 
        swe.subject_id = frr.subject_id 
    left join (
        select 
            fmwe.id,
            fmwe.fmwe_score,
            fmwe.word_id,
            fmwe.featured_major_id,
            m.ma_name,
            m.id as major_id
        from 
            filter_record as fr
        inner join 
            filter_record_regster as frr 
        on
            fr.id = frr.filter_id	
        inner join 	
            featured_major_wordcloud_entities as fmwe 
        on
            frr.word_id = fmwe.word_id 
        inner join 
            featured_majors as fm 
        on 
            fm.id = fmwe.featured_major_id
        inner join 
            majors as m 
        on 
            m.id = fm.major_id 
        where 	
            m.university_id = :university_id
            ) as cmwe
        on 
            cmwe.word_id = frr.word_id
        where 
            fr.id = :filter_id	
        ) as tab
    inner join 
        majors as m2 
    on 
        m2.id = tab.major_id
    group by 
        tab.featured_major_id,
        tab.ma_name,
        tab.major_id
    order by 
        sum(score) desc
       """
    stmt = text(query).bindparams(university_id=university_id, filter_id=filter_id)
    result = db.execute(stmt).all()
    return result
