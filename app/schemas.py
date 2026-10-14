from pydantic import BaseModel

class ProjectCreate(BaseModel):
    name: str
    description: str

class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    message: str