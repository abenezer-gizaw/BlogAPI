from .utils import *
from app.database import get_db
from app.routers.auth import get_current_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_ger_currenet_user

def test_all_post(add_user, add_post):
    response = client.get("/posts/all_posts")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": add_post.id,
            "title": "Test",
            "author": "test",
            "comments": [],
            "likes_count": 0
        }
    ]

def test_create_post(add_post):
   jason_data= {"title": "testing the book", "content": "this is the content"}
   response = client.post("/posts/create_post", json= jason_data)
   assert response.status_code== 204


