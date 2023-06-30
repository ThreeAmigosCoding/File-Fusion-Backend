from pydantic import BaseModel


class User(BaseModel):
    name: str
    last_name: str
    username: str
    email: str
    password: str
    date_of_birth: str


class UserLoginDTO(BaseModel):
    username: str
    password: str
