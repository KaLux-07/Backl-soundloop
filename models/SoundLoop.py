from pydantic import BaseModel

class SoundLoop(BaseModel):
    id: int
    name: str
    user_id: int