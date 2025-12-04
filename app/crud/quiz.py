from sqlalchemy.orm import Session
from app.models import Quiz
from app.schemas import QuizCreate

def create_quiz(quiz: QuizCreate, db: Session):
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

def get_quiz_analytics(id: int, db: Session):
    quiz = db.query(Quiz).filter(Quiz.id == id).first()
    if not quiz:
        return None
    
    completion_rate = (
        quiz.completed / quiz.attempts * 100
        if quiz.attempts > 0
        else 0.0
    )

    average_score = (
        quiz.total_score / quiz.completed
        if quiz.completed > 0
        else 0.0
    )

    average_time_spent = (
        quiz.total_time_spent / quiz.completed
        if quiz.completed > 0
        else 0.0
    )

    drop_off_rate = (
        (quiz.attempts - quiz.completed) / quiz.attempts * 100
        if quiz.attempts > 0
        else 0.0
    )
    
    return {
        "id": quiz.id,
        "completion_rate": completion_rate,
        "average_score": average_score,
        "average_time_spent": average_time_spent,
        "drop_off_rate": drop_off_rate,
        "created_at": quiz.created_at,
        "updated_at": quiz.updated_at
    }

def get_all_quiz_analytics(skip: int, limit: int, db: Session):
    quizzes = db.query(Quiz).offset(skip).limit(limit).all()
    return [get_quiz_analytics(quiz.id, db) for quiz in quizzes]

def update_quiz_analytics(id: int, analytics_data: dict, db: Session):
    db_quiz = get_quiz(id, db)
    if not db_quiz:
        return None

    for field, val in analytics_data.items():
        if hasattr(db_quiz, field):
            setattr(db_quiz, field, val)

    db.commit()
    db.refresh(db_quiz)
    return get_quiz_analytics(id, db)