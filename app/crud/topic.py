from sqlalchemy.orm import Session
from app.models import Topic
from app.schemas import TopicCreate

def create_topic(db: Session, topic: TopicCreate):
    db_topic = Topic(**topic.dict())
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic

def get_topics(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Topic).offset(skip).limit(limit).all()

def get_topic(db: Session, id: int):
    return db.query(Topic).filter(Topic.id == id).first()

def update_topic(db: Session, id: int, topic_data: dict):
    db_topic = get_topic(db, id)
    if not db_topic:
        return None

    for field, val, in topic_data.items():
        if hasattr(db_topic, field):
            setattr(db_topic, field, val)

    db.commit()
    db.refresh(db_topic)
    return db_topic

def delete_topic(db: Session, id: int):
    db_topic = get_topic(db, id)
    if not db_topic:
        return True

    db.delete(db_topic)
    db.commit()
    return True
