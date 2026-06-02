from pydantic import BaseModel

class new_user(BaseModel):
    first_name:str
    last_name:str
    username:str
    email: str
    password: str


class new_post(BaseModel):
    title:str
    content:str

class CommentCreate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: int
    content: str

    class Config:
        from_attributes = True