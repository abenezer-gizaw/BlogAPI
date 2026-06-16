#The goal is:
#user can like a post.
#user can unlike a post.
#user cannot like the same post twice.
#Each post can have many likes.
#Each user can like many posts.
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from.auth import get_current_user
from ..models import Like, Post
from typing import Annotated

router = APIRouter(
    prefix='/posts',
    tags=["likes"]
)

db_dependency = Annotated [Session, Depends(get_db)]
jwt_depencency = Annotated[dict, Depends(get_current_user)]
@router.post("/{post_id}/likes", status_code=200)
def like_post( post_id:int, db: db_dependency, user:jwt_depencency):
    if user is None:
        raise HTTPException( status_code=401, detail="Not authenticated")
    post = db.query(Post).filter( Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404,detail="Post not found")
    
    existing_like = db.query(Like).filter(Like.user_id == user.get('id'), Like.post_id == post_id).first()
    if existing_like:
        raise HTTPException(status_code=409, detail="Already liked")
    new_like = Like(user_id=user.get("id"), post_id=post_id)

    db.add(new_like)
    db.commit()
    return { "message": "Post liked successfully"} # i might need to add the name of the liked post
@router.delete("/{post_id}/unlike", status_code= 200)
def unlike_post(post_id: int, db: db_dependency, user:jwt_depencency):
    if user is None:
        raise HTTPException( status_code=401, detail="Not authenticated")
    like = db.query(Like).filter( Like.user_id == user.get("id"), Like.post_id == post_id).first()
    if not like:
        raise HTTPException (status_code=404, detail="Like not found")
    db.delete(like)
    db.commit()
    return {"message": "Like removed"}