from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas import TopicCreate, TopicUpdate, TopicResponse
from app.crud import create_topic, get_topic, get_topics, update_topic, delete_topic
from app.core import get_db, limiter

router = APIRouter(prefix="/topics")

@router.get("/", response_model=list[TopicResponse])
@limiter.limit("100/minute;1000/hour")
def get_topics_route(request: Request, skip: int=0, limit: int=100, db: Session=Depends(get_db)):
    topics = get_topics(skip, limit, db)
    if not topics:
        raise HTTPException(status_code=404, detail="No topic found")
    return topics

@router.get("/{id}", response_model=TopicResponse)
@limiter.limit("100/minute;1000/hour")
def get_topic_route(request: Request, id: int, db: Session=Depends(get_db)):
    topic = get_topic(id, db)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

@router.post("/", response_model=TopicResponse)
@limiter.limit("10/minute;100/hour")
def create_topic_route(request: Request, data: TopicCreate, db: Session=Depends(get_db)):
    try:
        topic = create_topic(data, db)
        return topic
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Topic already exists")

@router.patch("/{id}", response_model=TopicResponse)
@limiter.limit("5/minute;50/hour")
def update_topic_route(request: Request, id: int, data: TopicUpdate, db: Session=Depends(get_db)):
    topic = update_topic(id, data.model_dump(exclude_unset=True), db)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

@router.delete("/{id}")
@limiter.limit("5/minute;30/hour")
def delete_topic_route(request: Request, id: int, db: Session=Depends(get_db)):
    topic = get_topic(id, db)
    if not topic:
        return Response(status_code=204)
    delete_topic(id, db)
    return {"detail": "Topic deleted"}