from sqlalchemy.orm import Session
from app.models import Quiz
from app.schemas import QuizCreate

def create_quiz(data: QuizCreate, db: Session):
    db_quiz = Quiz(**quiz.model_dump())
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

def get_quizzes(skip: int, limit: int, db: Session):
    return db.query(Quiz).offset(skip).limit(limit).all()

def get_quiz(id: int, db: Session):
    return db.query(Quiz).filter(Quiz.id == id).first()

def update_quiz(id: int, quiz_data: dict, db: Session):
    db_quiz = get_quiz(id, db)
    if not db_quiz:
        return None

    for field, val in quiz_data.items():
        if hasattr(db_quiz, field):
            setattr(db_quiz, field, val)

def delete_quiz(id: int, db: Session):
    db_quiz = get_quiz(id, db)
    if not db_quiz:
        return True

    db.delete(db_quiz)
    db.commit()
    return True