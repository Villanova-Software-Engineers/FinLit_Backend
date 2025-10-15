from sqlalchemy.orm import Session
from app.models import Lesson
from app.schemas import LessonCreate

def create_lesson(db: Session, lesson: LessonCreate):
    ...

def get_lessons():
    ...

def get_lesson():
    ...

def update_lesson():
    ...

def delete_lesson():
    ...