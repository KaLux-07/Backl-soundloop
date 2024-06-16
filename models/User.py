from pydantic import BaseModel

class User(BaseModel):
    name: str
    surname: str
    email: str
    username: str
    password_hash: str