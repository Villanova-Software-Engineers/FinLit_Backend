from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas import UserCreate, UserResponse, UserUpdate
from app.crud import create_user, get_users, get_user, get_user_by_firebase_id, update_user, delete_user
from app.core import get_db, limiter

router = APIRouter(prefix="/users", tags=[Users])

@router.post("/", response_model=UserResponse)
@limiter.limit("10/minute;100/hour")
def create_user_route(data: UserCreate, db: Session = Depends(get_db())):
    try:
        user = create_user(data, db)
        return user
    except IntegrityError:
        db.rollback()
        existing = get_user_by_firebase_id(data.firebase_id, db)
        if existing:
            return existing
        raise HTTPException(status_code=409, detail="User already exists")

@router.get("/", response_model=list[UserResponse])
@limiter.limit("100/minute;1000/hour")
def get_users_router(skip: int, limit: int, db: Session = Depends(get_db())):
    users = get_users(skip, limit, db)

    if not users:
        raise HTTPException(status_code=404, detail="There are no users")

    return users

@router.get("/firebase/{firebase_id}", response_model=list[UserResponse])
@limiter.limit("100/minute;1000/hour")
def get_user_by_firebase_id_route(firebase_id: str, db: Session = Depends(get_db())):
    user = get_user_by_firebase_id(firebase_id, db)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.get("/", response_model=UserResponse)
@limiter.limit("100/minute;1000/hour")
def get_user_route(id: int, db: Session = Depends(get_db())):
    user = get_user(id, db)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.patch("/{id}", response_model=UserResponse)
@limiter.limit("5/minute;50/hour")
def update_user_route(id: int, user_data: UserUpdate, db: Session = Depends(get_db())):
    user = update_user(id, user_data.model_dump(exclude_unset=True), db)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.delete("/{id}", response_model=UserResponse)
@limiter.limit("5/minute;30/hour")
def delete_user_route(id: int, firebase_id: int, db: Session = Depends(get_db())):
    user = get_user(id, db)

    if not user:
        return Response(status_code=204)

    success = delete_user(id, firebase_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")

    return {"detail": "User deleted"}