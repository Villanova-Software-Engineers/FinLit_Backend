from sqlalchemy.orm import Session
from app.models import Lesson
from app.schemas import LessonCreate

def create_lesson(lesson: LessonCreate, db: Session):
    db_lesson = Lesson(**lesson.model_dump())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

def get_lessons(skip: int, limit: int, db: Session):
    return db.query(Lesson).offset(skip).limit(limit).all()

def get_lesson(id: int, db: Session):
    return db.query(Lesson).filter(Lesson.id == id).first()

def update_lesson(id: int, lesson_data: dict, db: Session):
    db_lesson = get_lesson(id, db)
    if not db_lesson:
        return None

    for field, val in lesson_data.items():
        if hasattr(db_lesson, field):
            setattr(db_lesson, field, val)

    db.commit()
    db.refresh(db_lesson)
    return db_lesson

def delete_lesson(id: int, db: Session):
    db_lesson = get_lesson(id, db)
    if not db_lesson:
        return True

    db.delete(db_lesson)
    db.commit()
    return True

def get_lesson_analytics(id: int, db: Session):
    return db.query(Lesson).filter(Lesson.id == id).first()

def get_all_lesson_analytics(skip: int, limit: int, db: Session):
    return db.query(Lesson).offset(skip).limit(limit).all()

def update_lesson_analytics(id: int, analytics_data: dict, db: Session):
    db_lesson = get_lesson(id, db)
    if not db_lesson:
        return None

    for field, val in analytics_data.items():
        if hasattr(db_lesson, field):
            setattr(db_lesson, field, val)

    db.commit()
    db.refresh(db_lesson)
    return db_lesson