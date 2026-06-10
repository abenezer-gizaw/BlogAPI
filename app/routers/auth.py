from fastapi import APIRouter, HTTPException, status, Depends
from ..schemas import new_user, UserResponse
from ..database import get_db
from ..models import User
from typing import Annotated
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

router = APIRouter(
    prefix="/auth",
    tags=['auth']
)
SECRET_KEY= 'JBDFKJABFI47789@5'
ALGORITHM ="HS256"

db_dependency = Annotated [Session, Depends(get_db)]
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated ="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def authentication(username:str, password:str, db:db_dependency):
    user_model = db.query(User).filter(User.username==username).first()
    if user_model is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="user doesn't exist")
    verify_result = pwd_context.verify(password, user_model.hashed_password)
    if verify_result is False:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="user doesn't exist")
    return {"username": user_model.username, "id": user_model.id}

def create_jwt_token (data:dict, expires_delta: timedelta): # 3 steps, copy the data from verified user
     #update it with the expiration time
     # pass it to jwt and get a return token
     to_encode = data.copy()

     expire = datetime.now(timezone.utc) + expires_delta
     to_encode.update({"exp": expire})
     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
     return encoded_jwt

def get_current_user (token:str =Depends(oauth2_scheme)):
    try:
        payload = jwt.decode (token,SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get ('username')
        user_id: int = payload.get ('id')
        if username is None or user_id is None:
            raise HTTPException (status_code= 401, detail= 'unuaturotized user')
        user_info = {'username':username, 'id': user_id}
        return user_info
    except JWTError:
         raise HTTPException(status_code=401, detail= 'Unauthorized user')


@router.get('/', response_model= list[UserResponse], status_code= status.HTTP_200_OK)
async def get_all_users(db:db_dependency):
    user = db.query(User).all()
    user_list=[]
    for each in user:
        user_list.append (UserResponse (id = each.id,username = each.username, email = each.email))
    return user_list

@router.post('/create_new', status_code= status.HTTP_204_NO_CONTENT)
async def create_new(user_input:new_user, db:db_dependency):
    create_user_model = User(first_name = user_input.first_name,
                           last_name = user_input.last_name,
                           username = user_input.username,
                           email=user_input.email,
                           hashed_password= pwd_context.hash(user_input.password))
    
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)

@router.post('/login', status_code= 200)
async def login(login_info: Annotated[OAuth2PasswordRequestForm,Depends()], db:db_dependency):
    user_dict= authentication(username=login_info.username, password = login_info.password, db=db)
    if user_dict is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="user doesn't exist")
    token = create_jwt_token(user_dict, timedelta(minutes=15))
    return {"access_token": token, "token_type": "bearer"}
