from sqlalchemy import create_engine, text, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool # this is new importing the sqlalchemy pool
from fastapi.testclient import TestClient
from app.database import Base
import pytest
from app.models import User, Post, Comment, Like
from app.main import app
from passlib.context import CryptContext

Test_SQLALCHEMY_DATABASE_URL='sqlite:///./testdb.db' 
engine = create_engine(Test_SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False},
                        poolclass= StaticPool) # new change about poolclass
TestSessionLocal = sessionmaker(autocommit =False, autoflush= False, bind =engine)

Base.metadata.create_all(bind=engine) # crate all the tables from base, and model is a child of base class from database

pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated ="auto")
def override_get_db ():
    db = TestSessionLocal()
    try: 
        yield db #this is actually interesting makes the database running till the route completed,
        #once it's done pass it to db.cloe  close the session 
    finally:
        db.close()

def override_ger_currenet_user():
    return {'username':'test', 'id':1 , 'user_role':'admin'}

client = TestClient(app) # this is how we force it to take this. new test new db and jwt dependency

@pytest.fixture
def add_user():
    db = TestSessionLocal()

    user = User(
        email="test",
        username="test",
        first_name="test",
        last_name="test",
        hashed_password=pwd_context.hash("test")
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    yield user

    db.query(User).delete()
    db.commit()
    db.close()

@pytest.fixture
def add_post(add_user):
    db = TestSessionLocal()

    post = Post(
        title="Test",
        content="Test",
        owner_id=add_user.id
    )

    db.add(post)
    db.commit()
    db.refresh(post)

    yield post

    db.query(Post).delete()
    db.commit()
    db.close()

@pytest.fixture
def add_comment(add_user, add_post):
    db = TestSessionLocal()
    add_comment = Comment(content="Test comment", user_id = add_user.id, post_id= add_post.id)
    db.add(add_comment)
    db.commit()
    db.refresh(add_comment)

    yield add_comment
    
    db.query(Comment).delete()
    db.commit()
    db.close()

@pytest.fixture
def add_like(add_user, add_post):
    db = TestSessionLocal()
    db.query(Like).delete()
    db.commit()

    add_like = Like(user_id = add_user.id, post_id = add_post.id)
    db.add(add_like)
    db.commit()
    db.refresh(add_like)

    yield add_like
    db.query(Like).delete()
    db.commit()
    db.close()
