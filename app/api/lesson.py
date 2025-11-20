from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas.lesson import LessonCreate, LessonUpdate, LessonResponse, LessonAnalyticsResponse, LessonAnalyticsUpdate
from app.crud.lesson import create_lesson, get_lesson, get_lessons, update_lesson, delete_lesson, update_lesson_analytics, get_lesson_analytics, get_all_lesson_analytics
from app.core import get_db

router = APIRouter()

@router.post("/lessons", response_model=LessonResponse)
def create_lesson_route(data: LessonCreate, db: Session=Depends(get_db)):
    try:
        lesson = create_lesson(data, db)
        return lesson
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Lesson already exists")

@router.get("/lessons", response_model=list[LessonResponse])
def get_lessons_route(skip: int=0, limit: int=100, db: Session=Depends(get_db)):
    lessons = get_lessons(skip, limit, db)
    if not lessons:
        raise HTTPException(status_code=404, detail="No lessons found")
    return lessons

@router.get("/lessons/{id}", response_model=LessonResponse)
def get_lesson_route(id: int, db: Session=Depends(get_db)):
    lesson = get_lesson(id, db)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson

@router.patch("/lessons{id}", response_model=LessonResponse)
def update_lesson_route(id: int, data: LessonUpdate, db: Session=Depends(get_db)):
    lesson = update_lesson(id, data.model_dump(exclude_unset=True), db)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson

@router.delete("/lessons/{id}")
def delete_lesson_route(id: int, db: Session=Depends(get_db)):
    lesson = get_lesson(id, db)
    if not lesson:
        return Response(status_code=204)

    delete_lesson(id, db)
    return {"detail": "Lesson deleted"}


@router.get("/lessons/{id}/analytics", response_model=LessonAnalyticsResponse)
def get_lesson_analytics_route(id: int, db: Session = Depends(get_db)):
    lesson = get_lesson_analytics(id, db)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    return lesson

@router.get("/lessons/analytics", response_model=list[LessonAnalyticsResponse])
def get_lessons_analytics_route(skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    lessons = get_all_lesson_analytics(skip, limit, db)
    if not lessons:
        raise HTTPException(status_code=404, detail="No lessons found")
    
    return lessons

@router.patch("/lessons/{id}/analytics", response_model=LessonAnalyticsResponse)
def update_lesson_analytics_route(id: int, data: LessonAnalyticsUpdate, db: Session = Depends(get_db)):
    lesson = update_lesson_analytics(id, data.model_dump(exclude_unset=True), db)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson