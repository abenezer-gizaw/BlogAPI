from .utils import *
from app.database import get_db
from app.routers.auth import authentication, create_jwt_token, ALGORITHM, SECRET_KEY, get_current_user
from fastapi import HTTPException
from jose import jwt
from datetime import timedelta, datetime, timezone
from starlette import status

app.dependency_overrides[get_db] = override_get_db
def test_create_user(add_user):
    jason_data ={'email' :'Tes@test.com',
                 'username' : 'Test',
                 'first_name' : 'Test',
                 'last_name' : 'Test',
                 'password' : 'bcrypt'}
    response = client.post('/auth/create_new', json = jason_data)
    assert response.status_code ==204


def test_authentication(add_user):
    test_db = TestSessionLocal()
    result = authentication(username='test', password='test',db=test_db)
    assert result.get('username')=='test'
    test_db.close()

def test_wrong_PW_authentication(add_user):
    test_db = TestSessionLocal()
    with pytest.raises(HTTPException) as exc:
        authentication(username='test', password='wrong_pw',db=test_db)
        assert exc.value.status_code == 404
    test_db.close()

def test_create_jwt ():
    user_data = {'sub': "test", 'id':"1"}
    time_pass = timedelta(minutes=15)
    token =  create_jwt_token(user_data,time_pass)
    payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
    assert payload.get('sub')==user_data.get('sub')
    assert payload.get('id')==user_data.get('id')


def test_get_current_user():
    user_data = {'username': "test", 'id':"1", 'user_role': "admin"}
    time_pass = datetime.now(timezone.utc) + timedelta(minutes=15)
    user_data.update ({"exp":time_pass})
    token = jwt.encode(user_data,SECRET_KEY, algorithm= ALGORITHM)
    out_put = get_current_user(token)
    assert out_put.get('username')== user_data.get ('username')

def test_find_all_user(add_user):
    response = client.get("/auth")
    assert response.status_code== status.HTTP_200_OK
    assert response.json() == [
        {
            "id": 1,
            "username": "test",
            "email": "test"
        }
    ]
def test_login(add_user):
    json_data= {"username": "test", "password": "test"}
    db_test = TestSessionLocal()
    response = client.post('/auth/login', data=json_data)
    assert response.status_code== 200
    assert response.json()["token_type"]=="bearer"