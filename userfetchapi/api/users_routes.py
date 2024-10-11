from typing import Generator, Sequence

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models.user_model import SessionLocal, User
from ..schemas.user_schemas import UserDatabaseSchema, UserSchema

router = APIRouter()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/users/gender/{gender}", response_model=Sequence[UserSchema])
def get_by_gender(gender: str, db: Session = Depends(get_db)) -> Sequence[UserSchema]:
    query = select(User).where(User.gender == gender)
    users = db.execute(query).scalars().all()

    if not users:
        raise HTTPException(status_code=404, detail="No users found")

    return users


@router.get("/users/age/")
@router.get("/users/age/{age}")
def get__by_age(age: int = 35, db: Session = Depends(get_db)) -> Sequence[UserSchema]:
    query = select(User).where(User.age == age)
    users = db.execute(query).scalars().all()

    if not users:
        raise HTTPException(status_code=404, detail="No users found")

    return users


@router.post("/users/gender_age")
def post_gender_age(
    gender: str = "male", age: int = 30, db: Session = Depends(get_db)
) -> Sequence[UserSchema]:
    query = select(User).where(User.gender == gender, User.age == age)
    users = db.execute(query).scalars().all()

    if not users:
        raise HTTPException(status_code=404, detail="No users found")

    return users


@router.get("/users/gender_age")
def get_gender_age(
    gender: str = "male", age: int = 30, db: Session = Depends(get_db)
) -> Sequence[UserSchema]:
    query = select(User).where(User.gender == gender, User.age == age)
    users = db.execute(query).scalars().all()

    if not users:
        raise HTTPException(status_code=404, detail="No users found")

    return users


@router.post("/users", response_model=UserDatabaseSchema)
def create_user(user: UserSchema, db: Session = Depends(get_db)) -> UserDatabaseSchema:
    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        gender=user.gender,
        age=user.age,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
