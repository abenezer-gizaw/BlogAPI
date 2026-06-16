from fastapi import APIRouter, Depends, HTTPException
from ..database import get_db
from .auth import get_current_user
from typing import Annotated
from sqlalchemy.orm import Session, joinedload
from ..models import User, Post, Like,Comment
from ..schemas import new_post, PostResponse


router = APIRouter(prefix="/posts",
                   tags=["posts"])
db_dependency = Annotated [Session, Depends(get_db)]
jwt_depencency = Annotated[dict, Depends(get_current_user)]

@router.get('/all_posts', response_model= list[PostResponse], status_code= 200)

async def all_posts(user: jwt_depencency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="User is not authenticated.")

    posts = (
        db.query(Post)
        .options(
            joinedload(Post.owner),
            joinedload(Post.comments).joinedload(Comment.user)
        )
        .all()
    )

    result = []

    for post in posts:
        likes_count = (db.query(Like).filter(Like.post_id == post.id).count())

        result.append(
        PostResponse(id=post.id,title=post.title,author=post.owner.username,comments=post.comments,likes_count=likes_count)
)
    return result
    

@router.get('/{post_id}', response_model= PostResponse, status_code= 200)
async def get_post(post_id:int, user:jwt_depencency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    post = (
    db.query(Post)
    .options(
        joinedload(Post.owner),
        joinedload(Post.comments).joinedload(Comment.user)
    )
    .filter(Post.id == post_id)
    .first()
)

    if not post:
        raise HTTPException(status_code=404,detail="Post not found")

    likes_count = (db.query(Like).filter(Like.post_id == post.id).count())

    return PostResponse(
        id=post.id,
        title=post.title,
        author=post.owner.username,
        comments=post.comments,
        likes_count=likes_count
    )
@router.post('/create_post', status_code= 204)
async def create_post(post:new_post, user:jwt_depencency, db:db_dependency):
    if user is None:
        raise HTTPException (status_code=401, detail= "User is not authenticated.")
    post = Post(**post.model_dump(),owner_id = user.get('id'))
    db.add(post)
    db.commit()
    db.refresh(post)

@router.put('/update_post/{post_id}', status_code=200)
async def update_post(post_id:int,update:new_post,user:jwt_depencency, db:db_dependency):
    if user is None:
        raise HTTPException (status_code=401, detail= "Authentication is required")
    post_obj = db.query(Post). filter(post_id==Post.id, user.get('id')==Post.owner_id).first()
    if post_obj is None:
        raise HTTPException(status_code=404, detail="Post is not found")
    post_obj.content = update.content
    post_obj.title=update.title
    db.commit()
    db.refresh(post_obj)
    return post_obj

@router.delete("/delete_post/{post_id}", status_code=204)
async def delete_post(post_id:int, user:jwt_depencency, db:db_dependency):
    if user is None:
        raise HTTPException (status_code=401, detail= "Authentication is required")
    post_obj = db.query(Post).filter(Post.id == post_id, Post.owner_id == user.get("id")).first()
    if post_obj is None:
        raise HTTPException(status_code=404, detail="Post is not found")
    db.delete(post_obj)
    db.commit()
    return {"message": "Post deleted successfully"}

