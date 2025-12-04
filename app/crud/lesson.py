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
    lesson = db.query(Lesson).filter(Lesson.id == id).first()
    if not lesson:
        return None
    
    completion_rate = (
        lesson.completed / lesson.attempts * 100
        if lesson.attempts > 0
        else 0.0
    )

    average_time_spent = (
        lesson.total_time_spent / lesson.completed
        if lesson.completed > 0
        else 0.0
    )

    quiz_aggregate_score = (
        lesson.total_quiz_score / lesson.num_quizzes
        if lesson.completed > 0
        else 0.0
    )

    drop_off_rate = (
        (lesson.attempts - lesson.completed) / lesson.attempts * 100
        if lesson.attempts > 0
        else 0.0
    )

    return {
        "id": lesson.id,
        "completion_rate": completion_rate,
        "average_time_spent": average_time_spent,
        "quiz_aggregate_score": quiz_aggregate_score,
        "drop_off_rate": drop_off_rate,
        "created_at": lesson.created_at,
        "updated_at": lesson.updated_at
    }

def get_all_lesson_analytics(skip: int, limit: int, db: Session):
    lessons = db.query(Lesson).offset(skip).limit(limit).all()
    return [get_lesson_analytics(lesson.id, db) for lesson in lessons]

def update_lesson_analytics(id: int, analytics_data: dict, db: Session):
    db_lesson = get_lesson(id, db)
    if not db_lesson:
        return None

    for field, val in analytics_data.items():
        if hasattr(db_lesson, field):
            setattr(db_lesson, field, val)

    db.commit()
    db.refresh(db_lesson)
    return get_lesson_analytics(id, db)