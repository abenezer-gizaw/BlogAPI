from pydantic import BaseModel

class new_user(BaseModel):
    first_name:str
    last_name:str
    username:str
    email: str
    password: str