from sqlalchemy.orm import Session
from app.models import Topic
from app.schemas import TopicCreate

def create_topic(topic: TopicCreate, db: Session):
    db_topic = Topic(**topic.model_dump())
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic

def get_topics(skip: int, limit: int, db: Session):
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

def get_topic_analytics(id: int, db: Session):
    topic = db.query(Topic).filter(Topic.id == id).first()
    if not topic:
        return None
    
    completion_rate = (
        topic.completed / topic.attempts * 100
        if topic.attempts > 0
        else 0.0
    )

    average_time_spent = (
        topic.total_time_spent / topic.completed
        if topic.completed > 0
        else 0.0
    )

    average_score = (
        topic.total_score / topic.completed
        if topic.completed > 0
        else 0.0
    )

    drop_off_rate = (
        (topic.attempts - topic.completed) / topic.attempts * 100
        if topic.attempts > 0
        else 0.0
    )

    return {
        "id": topic.id,
        "completion_rate": completion_rate,
        "average_time_spent": average_time_spent,
        "average_score": average_score,
        "drop_off_rate": drop_off_rate,
        "created_at": topic.created_at,
        "updated_at": topic.updated_at
    }

def get_all_topic_analytics(skip: int, limit: int, db: Session):
    topics = db.query(Topic).offset(skip).limit(limit).all()
    return [get_topic_analytics(topic.id, db) for topic in topics]

def update_topic_analytics(id: int, analytics_data: dict, db: Session):
    db_topic = get_topic(id, db)
    if not db_topic:
        return None

    for field, val in analytics_data.items():
        if hasattr(db_topic, field):
            setattr(db_topic, field, val)

    db.commit()
    db.refresh(db_topic)
    return get_topic_analytics(id, db)