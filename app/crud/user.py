from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate
from firebase_admin import auth

def create_user(user: UserCreate, db: Session):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh()
    return db_user

def get_users(skip: int, limit: int, db: Session):
    return db.query(User).offset(skip).limit(limit).all()

def get_user(id: int, db: Session):
    return db.query(User).filter(User.id == id).first()

def get_user_by_firebase_id(firebase_id: str, db: Session):
    return db.query(User).filter(User.firebase_id == firebase_id).first()

def update_user(id: int, user_data: dict, db: Session):
    db_user = db.query(User).filter(User.id == id).first()
    if not db_user:
        return None

    for field, value in user_data.items():
        if hasattr(db_user, field):
            setattr(db_user, field, value)

    db.commit()
    db.refresh()
    return db_user

def delete_user(id: int, firebase_id: str, db: Session):
    try:
        auth.delete_user(firebase_id)
    except Exception as e:
        pass

    db_user = db.query(User).filter(User.id == id).first()
    if not db_user:
        return False

    db.delete(db_user)
    db.commit()
    return True


