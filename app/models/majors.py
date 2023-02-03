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


class Major(Base):
    __tablename__ = "majors"
    id = Column(BigInteger, primary_key=True)
    creation_time = Column(DateTime(timezone=True), server_default=func.utcnow())
    update_time = Column(DateTime(timezone=True), server_default=func.utcnow())
    category_id = Column(BigInteger)
    university_id = Column(BigInteger)
    ma_name = Column(String)
    ma_code = Column(String)
    ma_school_major_code = Column(String)
    ma_day_night_code = Column(String)
    ma_day_night_name = Column(String)
    ma_curriculum_code = Column(String)
    ma_curriculum_name = Column(String)
    cn_major_id = Column(BigInteger)
    is_active = Column(Boolean)
    ma_active_status_name = Column(String)


class Major_detail_infos(Base):
    __tablename__ = "major_detail_infos"
    id = Column(BigInteger, primary_key=True)
    major_id = Column(BigInteger)
    year = Column(Integer)
    admission_quota = Column(Integer)
    num_students = Column(Integer)
    competition_rate = Column(Float)
    employment_rate = Column(Float)
    tuition = Column(Float)
    scholarship = Column(Float)


class Major_categories(Base):
    __tablename__ = "major_categories"
    id = Column(BigInteger, primary_key=True)
    creation_time = Column(DateTime(timezone=True), server_default=func.utcnow())
    update_time = Column(DateTime(timezone=True), server_default=func.utcnow())
    category_small_name = Column(String(50))
    category_small_code = Column(String(10))
    category_middle_name = Column(String(50))
    category_middle_code = Column(String(10))
    category_large_name = Column(String(20))
    category_large_code = Column(String(5))


class Cn_majors(Base):
    __tablename__ = "cn_majors"
    id = Column(BigInteger, primary_key=True)
    creation_time = Column(DateTime(timezone=True), server_default=func.utcnow())
    update_time = Column(DateTime(timezone=True), server_default=func.utcnow())
    cn_l_class = Column(String(20))
    cn_major_seq = Column(BigInteger)
    cn_m_class = Column(String(20))
    cn_salary = Column(String(50))
    cn_employment = Column(String(50))
    cn_summary = Column(Text)
    cn_interest = Column(Text)
    cn_property = Column(Text)
    extras = Column(JSONB)
    embedding_vector = Column(JSONB)
    coord = Column(JSONB)


class Cn_related_majors(Base):
    __tablename__ = "cn_related_majors"
    id = Column(BigInteger, primary_key=True)
    creation_time = Column(DateTime(timezone=True), server_default=func.utcnow())
    update_time = Column(DateTime(timezone=True), server_default=func.utcnow())
    cn_major_id = Column(BigInteger)
    cnrm_name = Column(String(50))


class Cn_major_wordcloud_entities(Base):
    __tablename__ = "cn_major_wordcloud_entities"
    id = Column(BigInteger, primary_key=True)
    cmwe_score = Column(Float)
    cn_major_id = Column(BigInteger)
    word_id = Column(BigInteger)


class Featured_majors(Base):
    __tablename__ = "featured_majors"
    id = Column(BigInteger, primary_key=True)
    university_name = Column(String(100))
    name = Column(String(200))
    text_lect = Column(Text)
    text_intr = Column(Text)
    extras = Column(JSONB)
    embedding_vector = Column(JSONB)
    major_id = Column(BigInteger)


class Adiga_majors(Base):
    __tablename__ = "adiga_majors"
    id = Column(BigInteger, primary_key=True)
    year = Column(Integer)
    rcu_cd = Column(String(20))
    name = Column(String(100))
    num_students = Column(Integer)
    early_decision_competition_rate = Column(Float)
    regular_decision_competition_rate = Column(Float)
    student_book_grade_mean = Column(Float)
    featured_major_id = Column(BigInteger)
    university_tmp_id = Column(BigInteger)
    university_id = Column(BigInteger)
    major_id = Column(BigInteger)


def major_recommend_list(db: Session, university_id=0, filter_id=10):
    query = """
select 
	sum(score) as score,
	tab.featured_major_id,
	tab.ma_name,
	tab.major_id,
	tab.employment_rate,
	tab.admission_quota,
	tab.competition_rate
from (select 	
        case when cmwe.fmwe_score > 0 then cmwe.fmwe_score*(frr.fr_value/100::float) else swe.fmse_score *(frr.fr_value/100::float) end as score,
        frr.fr_value,
        frr.id,
        case when swe.featured_major_id  is null then cmwe.featured_major_id  else swe.featured_major_id end as featured_major_id,
        case when swe."name"  is null then cmwe."name"  else swe."name" end as ma_name,
        case when swe.major_id  is null then cmwe.major_id  else swe.major_id end as major_id,
        case when swe.employment_rate  is null then cmwe.major_id  else swe.employment_rate end as employment_rate,
        case when swe.admission_quota  is null then cmwe.admission_quota  else swe.admission_quota end as admission_quota,
        case when swe.competition_rate  is null then cmwe.competition_rate  else swe.competition_rate end as competition_rate
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
            m."name",
            m.employment_rate,
            m.admission_quota,
            m.competition_rate,
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
            v_majors as m 
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
            m."name",
            m.employment_rate,
            m.admission_quota,
            m.competition_rate,
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
            v_majors as m 
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
        tab.major_id,
        tab.employment_rate,
        tab.admission_quota,
        tab.competition_rate
    order by 
        sum(score) desc
       """
    stmt = text(query).bindparams(university_id=university_id, filter_id=filter_id)
    result = db.execute(stmt).all()
    return result
