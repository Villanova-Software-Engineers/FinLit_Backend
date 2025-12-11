from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas.topic import TopicCreate, TopicUpdate, TopicResponse, TopicAnalyticsResponse, TopicAnalyticsUpdate
from app.crud.topic import create_topic, get_topic, get_topics, update_topic, delete_topic, get_topic_analytics, get_all_topic_analytics, update_topic_analytics
from app.core import get_db

router = APIRouter(prefix="/topics", tags=["Topics"])

@router.get("/", response_model=list[TopicResponse])
@limiter.limit("100/minute;1000/hour")
async def get_topics_route(request: Request, skip: int=0, limit: int=100, db: Session=Depends(get_db)):
    topics = get_topics(skip, limit, db)
    if not topics:
        raise HTTPException(status_code=404, detail="No topic found")
    return topics

@router.get("/{id}", response_model=TopicResponse)
@limiter.limit("100/minute;1000/hour")
async def get_topic_route(request: Request, id: int, db: Session=Depends(get_db)):
    topic = get_topic(id, db)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

@router.post("/", response_model=TopicResponse)
@limiter.limit("10/minute;100/hour")
async def create_topic_route(request: Request, data: TopicCreate, db: Session=Depends(get_db)):
    try:
        topic = create_topic(data, db)
        return topic
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Topic already exists")

@router.patch("/{id}", response_model=TopicResponse)
@limiter.limit("5/minute;50/hour")
async def update_topic_route(request: Request, id: int, data: TopicUpdate, db: Session=Depends(get_db)):
    topic = update_topic(id, data.model_dump(exclude_unset=True), db)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

@router.delete("/{id}")
@limiter.limit("5/minute;30/hour")
async def delete_topic_route(request: Request, id: int, db: Session=Depends(get_db)):
    topic = get_topic(id, db)
    if not topic:
        return Response(status_code=204)
    delete_topic(id, db)
    return {"detail": "Topic deleted"}


@router.get("/{id}/analytics", response_model=TopicAnalyticsResponse)
@limiter.limit("100/minute;1000/hour")
def get_topic_analytics_route(request: Request, id: int, db: Session = Depends(get_db)):
    topic = get_topic_analytics(id, db)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    return topic

@router.get("/analytics", response_model=list[TopicAnalyticsResponse])
@limiter.limit("100/minute;1000/hour")
def get_topics_analytics_route(request: Request, skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    topics = get_all_topic_analytics(skip, limit, db)
    if not topics:
        raise HTTPException(status_code=404, detail="No topics found")
    
    return topics

@router.patch("/{id}/analytics", response_model=TopicAnalyticsResponse)
@limiter.limit("5/minute;50/hour")
def update_topic_analytics_route(request: Request, id: int, data: TopicAnalyticsUpdate, db: Session = Depends(get_db)):
    topic = update_topic_analytics(id, data.model_dump(exclude_unset=True), db)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic
