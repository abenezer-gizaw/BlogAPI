from fastapi import FastAPI
from .database import engine
from .models import Base
from .routers import auth, posts,comments,likes
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from.dependecies import limiter


Base.metadata.create_all(bind=engine) # table creation happen here, and if the table doesn't exist in models, it creates it when we run the program
# crete_all works to create the tables if it's not already created
app = FastAPI()
app.state.limiter =limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(likes.router)

@app.get('/', status_code= 200)
async def testing_setup():
    return{'message': 'setup all good'}