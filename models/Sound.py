from pydantic import BaseModel

class Sound(BaseModel):
    sound: bytes
    loop_id: int
    user_id: int