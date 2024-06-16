from pydantic import BaseModel

class Loop(BaseModel):
    loop_name: str
    user_id: int