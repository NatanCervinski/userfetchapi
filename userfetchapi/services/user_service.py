from pprint import pprint
from typing import List

import requests
from sqlalchemy.orm import Session

from ..models.user_model import User
from ..schemas.user_schemas import UserSchema


def fetch_random_users(count: int = 100) -> List[UserSchema]:
    url = "https://randomuser.me/api/"
    users = []
    for _ in range(count):
        response = requests.get(url)
        if response.status_code != 200:
            continue
        user_data = response.json().get("results", [])
        for user in user_data:
            user_schema = UserSchema(
                gender=user["gender"],
                age=user["dob"]["age"],
                first_name=user["name"]["first"],
                last_name=user["name"]["last"],
            )
            users.append(user_schema)
    return users


def populate_database_with_users(db: Session, users: List[UserSchema]) -> None:
    for user in users:
        new_user = User(
            gender=user.gender,
            age=user.age,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        db.add(new_user)
    db.commit()


def verify_database(db: Session) -> int:
    users = db.query(User).count()
    return users


def fetch_and_store_users(db: Session, count: int = 100) -> None:
    users = fetch_random_users(count)
    populate_database_with_users(db, users)
