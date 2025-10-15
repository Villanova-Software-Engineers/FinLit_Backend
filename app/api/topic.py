from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas import TopicCreate, TopicUpdate, TopicResponse
from app.crud import create_topic, get_topic, get_topics, update_topic, delete_topic
from app.core import get_db

router = APIRouter()

@router.post("/topics", response_model=TopicResponse)
def create_topic_route(data: TopicCreate, db: Session=Depends(get_db)):
    try:
        topic = create_topic(db, data)
        return topic
    except IntegrityError:
        db.rollback()
        existing = get_topic(db, data.id)
        if existing:
            return existing
        raise HTTPException(status_code=409, detail="Topic already exists")

@router.get("/topics", response_model=list[TopicResponse])
def get_topics_route(skip: int=0, limit: int=100, db: Session=Depends(get_db)):
    topics = get_topics(db, skip, limit)
    if not topics:
        raise HTTPException(status_code=404, detail="There are no topics")
    return topics

@router.get("/topics/{id}", response_model=TopicResponse)
def get_topic_route(id: int, db: Session=Depends(get_db)):
    topic = get_topic(db, id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

@router.patch("/topics{id}", response_model=TopicResponse)
def update_topic_route(id: int, data: TopicUpdate, db: Session=Depends(get_db)):
    topic = update_topic(db, id, data.model_dump(exclude_unset=True))
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not fouind")
    return topic

@router.delete("/topics/{id}")
def delete_topic_route(id: int, db: Session=Depends(get_db)):
    topic = get_topic(db, id)
    if not topic:
        return Response(status_code=204)

    success = delete_topic(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Topic not found")

    return {"detail": "Topic deleted"}
