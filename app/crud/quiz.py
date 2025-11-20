from sqlalchemy.orm import Session
from app.models import Quiz
from app.schemas import QuizCreate

<<<<<<< HEAD
def create_quiz(quiz: QuizCreate, db: Session):
    db_quiz = Quiz(**quiz.model_dump())
=======
def create_quiz(data: QuizCreate, db: Session):
    db_quiz = Quiz(**data.model_dump())
>>>>>>> 1ff98abaf46048b38da929f8380a22edc29c617d
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

def get_quiz_analytics(id: int, db: Session):
    return db.query(Quiz).filter(Quiz.id == id).first()

def get_all_quiz_analytics(skip: int, limit: int, db: Session):
    return db.query(Quiz).offset(skip).limit(limit).all()

def update_quiz_analytics(id: int, analytics_data: dict, db: Session):
    db_quiz = get_quiz(id, db)
    if not db_quiz:
        return None

    for field, val in analytics_data.items():
        if hasattr(db_quiz, field):
            setattr(db_quiz, field, val)

    db.commit()
    db.refresh(db_quiz)
    return db_quiz