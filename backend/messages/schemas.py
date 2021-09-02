from pydantic import BaseModel

class MessageCreate(BaseModel):
    message: str

class MessageSelect(BaseModel):
    message: str
