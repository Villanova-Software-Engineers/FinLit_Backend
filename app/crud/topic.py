from sqlalchemy.orm import Session
from app.models import Topic
from app.schemas import TopicCreate

def create_topic(topic: TopicCreate, db: Session):
    db_topic = Topic(**topic.model_dump())
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic

def get_topics(skip: int=0, limit: int=100, db: Session):
    return db.query(Topic).offset(skip).limit(limit).all()

def get_topic(id: int, db: Session):
    return db.query(Topic).filter(Topic.id == id).first()

def update_topic(id: int, topic_data: dict, db: Session):
    db_topic = get_topic(id, db)
    if not db_topic:
        return None

    for field, val, in topic_data.items():
        if hasattr(db_topic, field):
            setattr(db_topic, field, val)

    db.commit()
    db.refresh(db_topic)
    return db_topic

def delete_topic(id: int, db: Session):
    db_topic = get_topic(id, db)
    if not db_topic:
        return True

    db.delete(db_topic)
    db.commit()
    return True
