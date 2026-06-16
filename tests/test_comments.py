from .utils import *
from fastapi.testclient import TestClient
from app.database import get_db
from app.routers.auth import get_current_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_ger_currenet_user



def test_create_comment(add_comment):
    payload = {"content": "Add another comment"}
    response = client.post('/posts/1/comments', json = payload)
    assert response.status_code ==201
    assert response.json()== {'id': 2, 'content': 'Add another comment', 'user': {'id': 1, 'username': 'test'}}


def test_get_comments(add_comment):
    response = client.get('/posts/1/comments')
    assert response.status_code == 200
    assert response.json()== [{'id': 1, 'content': 'Test comment', 'user': {'id': 1, 'username': 'test'}}]

def test_update_commnet(add_comment):
    payload = {"content": "updated comment"} 
    response = client.put('/posts/comments/1', json = payload)
    assert response.status_code==200
    assert response.json()== {'id': 1, 'content': 'updated comment', 'user': {'id': 1, 'username': 'test'}}

def test_delete_comment(add_comment):
    response = client.delete('/posts/comments/1')
    response.status_code == 204