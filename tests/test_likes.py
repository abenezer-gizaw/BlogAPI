from .utils import *
from app.database import get_db
from app.routers.auth import get_current_user
from app.models import Like

app.dependency_overrides[get_db]= override_get_db
app.dependency_overrides[get_current_user]= override_ger_currenet_user

def test_like_post(add_post):
    db = TestSessionLocal()
    all_likes = db.query(Like).all()
    for each in all_likes:
        db.delete(each)
    db.commit()
    response = client.post('/posts/1/likes')
    assert response.status_code == 200
    assert response.json()== {'message': 'Post liked successfully'}

def test_unlike_post(add_like):
    response = client.delete("/posts/1/unlike")
    assert response.status_code ==200
    assert response.json() == {'message': 'Like removed'}