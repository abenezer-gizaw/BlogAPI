from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Comment, Post
from ..schemas import CommentCreate, CommentResponse
from .auth import get_current_user
from typing import Annotated

router = APIRouter(prefix="/posts", tags=["Comments"])
db_dependency = Annotated [Session, Depends(get_db)]
jwt_depencency = Annotated[dict, Depends(get_current_user)]

@router.post("/{post_id}/comments", response_model=CommentResponse, status_code= 201)
def create_comment(post_id: int,comment: CommentCreate,db:db_dependency,user:jwt_depencency):
    if user is None:
        raise HTTPException(status_code= 401, detail="User is not authenticated")
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = Comment(
        content=comment.content,
        post_id=post_id,
        user_id=user.get('id')
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment

@router.get("/{post_id}/comments", response_model=list[CommentResponse], status_code= 200)
def get_comments(post_id: int, db:db_dependency, user:jwt_depencency):
    if user is None:
        raise HTTPException(status_code= 401, detail="User is not authenticated")
    comments = db.query(Comment).filter(Comment.post_id == post_id).all()
    return comments

@router.put("/comments/{comment_id}", response_model=CommentResponse, status_code= 200)
def update_comment(comment_id: int,updated_comment: CommentCreate, db: db_dependency,user:jwt_depencency):
    if user is None:
        raise HTTPException(status_code= 401, detail="User is not authenticated")
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != user.get('id'):
        raise HTTPException(status_code=403, detail="Not authorized")

    comment.content = updated_comment.content

    db.commit()
    db.refresh(comment)

    return comment
@router.delete("/comments/{comment_id}", status_code=204)
def delete_comment(comment_id: int, db:db_dependency, user:jwt_depencency ):
    if user is None:
        raise HTTPException(status_code= 401, detail="User is not authenticated")
    
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != user.get('id'):
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(comment)
    db.commit()