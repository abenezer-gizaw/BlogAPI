from fastapi import FastAPI
from .database import engine
from .models import Base

Base.metadata.create_all(bind=engine) # table creation happen here, and if the table doesn't exist in models, it creates it when we run the program
# crete_all works to create the tables if it's not already created
app = FastAPI()


@app.get('/')
async def testing_setup():
    return{'message': 'setup all good'}