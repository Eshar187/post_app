from fastapi import FastAPI,Depends
from typing import List
from  login  import model
from login.database import engine,get_db,Base
from login.routers import login, auth, post, vote
# from .config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# model.Base.metadata.create_all(bind=engine)

origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# while True:  
@app.get('/')
def root():
    return {'message':'Hello World'}


app.include_router(login.router)
app.include_router(auth.router)
app.include_router(post.router)
app.include_router(vote.router)
