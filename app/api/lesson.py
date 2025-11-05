from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas import LessonCreate, LessonUpdate, LessonResponse
from app.crud import create_lesson, get_lesson, get_lessons, update_lesson, delete_lesson
from app.core import get_db, limiter

router = APIRouter(prefix="/lessons")

@router.get("/", response_model=list[LessonResponse])
@limiter.limit("100/minute;1000/hour")
def get_lessons_route(request: Request, skip: int=0, limit: int=100, db: Session=Depends(get_db)):
    lessons = get_lessons(skip, limit, db)
    if not lessons:
        raise HTTPException(status_code=404, detail="No lessons found")
    return lessons

@router.get("/{id}", response_model=LessonResponse)
@limiter.limit("100/minute;1000/hour")
def get_lesson_route(request: Request, id: int, db: Session=Depends(get_db)):
    lesson = get_lesson(id, db)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson

@router.post("/", response_model=LessonResponse)
@limiter.limit("10/minute;100/hour")
def create_lesson_route(request: Request, data: LessonCreate, db: Session=Depends(get_db)):
    try:
        lesson = create_lesson(data, db)
        return lesson
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Lesson already exists")

@router.patch("/{id}", response_model=LessonResponse)
@limiter.limit("5/minute;50/hour")
def update_lesson_route(request: Request, id: int, data: LessonUpdate, db: Session=Depends(get_db)):
    lesson = update_lesson(id, data.model_dump(exclude_unset=True), db)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson

@router.delete("/{id}")
@limiter.limit("5/minute;30/hour")
def delete_lesson_route(request: Request, id: int, db: Session=Depends(get_db)):
    lesson = get_lesson(id, db)
    if not lesson:
        return Response(status_code=204)
    delete_lesson(id, db)
    return {"detail": "Lesson deleted"}