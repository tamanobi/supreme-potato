from pydantic import BaseModel

class ClientCreate(BaseModel):
    key: str

class ClientSelect(BaseModel):
    key: str
