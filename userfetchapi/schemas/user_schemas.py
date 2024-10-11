from pydantic import BaseModel


class UserSchema(BaseModel):
    first_name: str
    last_name: str
    age: int
    gender: str


class UserDatabaseSchema(UserSchema):
    id: int
