from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas import QuizCreate, QuizUpdate, QuizResponse
from app.crud import create_quiz, get_quiz, get_quizzes, update_quiz, delete_quiz
from app.core import get_db, limiter

router = APIRouter()

@router.get("/quizzes", response_model=list[QuizResponse])
@limiter.limit("100/minute;1000/hour")
def get_quizzes_route(request: Request, skip: int, limit: int, db: Session=Depends(get_db)):
    quizzes = get_quizzes(skip, limit, db)
    if not quizzes:
        raise HTTPException(status_code=404, detail="No quizzes found")
    return quizzes

@router.get("/quizzes/{id}", response_model=QuizResponse)
@limiter.limit("100/minute;1000/hour")
def get_quiz_route(request: Request, id: int, db: Session=Depends(get_db)):
    quiz = get_quiz(id, db)
    if not quiz:
        raise HTTPException(status_code=404, detail="No quizzes found")
    return quiz

@router.post("/quizzes", response_model=QuizResponse)
@limiter.limit("10/minute;100/hour")
def create_quiz_route(request: Request, data: QuizCreate, db: Session=Depends(get_db)):
    try:
        quiz = create_quiz(data, db)
        return quiz
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Quiz already exists")

@router.patch("/quizzes/{id}", response_model=QuizResponse)
@limiter.limit("5/minute;50/hour")
def update_quiz_route(request: Request, id: int, data: QuizUpdate ,db: Session=Depends(get_db)):
    quiz = update_quiz(id, data.model_dump(exclude_unset=True), db)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz

@router.delete("/quizzes/{id}")
@limiter.limit("5/minute;30/hour")
def delete_quiz_route(request: Request, id: int, db: Session=Depends(get_db)):
    quiz = get_quiz(id, db)
    if not quiz:
        return Response(status_code=204)
    delete_quiz(id, db)
    return {"detail": "Quiz deleted"}