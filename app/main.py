from fastapi import FastAPI
from .database import engine
from .models import Base
from .routers import auth, posts,comments,likes


Base.metadata.create_all(bind=engine) # table creation happen here, and if the table doesn't exist in models, it creates it when we run the program
# crete_all works to create the tables if it's not already created
app = FastAPI()
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(likes.router)

@app.get('/')
async def testing_setup():
    return{'message': 'setup all good'}