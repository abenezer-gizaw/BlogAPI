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

class CommentUser(BaseModel):
    id: int
    username: str

    model_config = {
        "from_attributes": True
    }


class CommentResponse(BaseModel):
    id: int
    content: str
    user: CommentUser

    class Config:
        from_attributes = True

class LikeRequest(BaseModel):
    post_id: int
    
class PostResponse(BaseModel):
    id: int
    title: str
    author: str
    comments: list[CommentResponse]
    likes_count: int

    model_config = {"from_attributes": True}
