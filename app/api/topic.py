from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas.topic import TopicCreate, TopicUpdate, TopicResponse, TopicAnalyticsResponse, TopicAnalyticsUpdate
from app.crud.topic import create_topic, get_topic, get_topics, update_topic, delete_topic, get_topic_analytics, get_all_topic_analytics, update_topic_analytics
from app.core import get_db

router = APIRouter()

@router.post("/topics", response_model=TopicResponse)
def create_topic_route(data: TopicCreate, db: Session=Depends(get_db)):
    try:
        topic = create_topic(data, db)
        return topic
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Topic already exists")

@router.get("/topics", response_model=list[TopicResponse])
def get_topics_route(skip: int=0, limit: int=100, db: Session=Depends(get_db)):
    topics = get_topics(skip, limit, db)
    if not topics:
        raise HTTPException(status_code=404, detail="No topic found")
    return topics

@router.get("/topics/{id}", response_model=TopicResponse)
def get_topic_route(id: int, db: Session=Depends(get_db)):
    topic = get_topic(id, db)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

@router.patch("/topics{id}", response_model=TopicResponse)
def update_topic_route(id: int, data: TopicUpdate, db: Session=Depends(get_db)):
    topic = update_topic(id, data.model_dump(exclude_unset=True), db)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

@router.delete("/topics/{id}")
def delete_topic_route(id: int, db: Session=Depends(get_db)):
    topic = get_topic(id, db)
    if not topic:
        return Response(status_code=204)

    delete_topic(id, db)
    return {"detail": "Topic deleted"}


@router.get("/topics/{id}/analytics", response_model=TopicAnalyticsResponse)
def get_topic_analytics_route(id: int, db: Session = Depends(get_db)):
    topic = get_topic_analytics(id, db)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    return topic

@router.get("/topics/analytics", response_model=list[TopicAnalyticsResponse])
def get_topics_analytics_route(skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    topics = get_all_topic_analytics(skip, limit, db)
    if not topics:
        raise HTTPException(status_code=404, detail="No topics found")
    
    return topics

@router.patch("/topics/{id}/analytics", response_model=TopicAnalyticsResponse)
def update_topic_analytics_route(id: int, data: TopicAnalyticsUpdate, db: Session = Depends(get_db)):
    topic = update_topic_analytics(id, data.model_dump(exclude_unset=True), db)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic