from fastapi import APIRouter, Depends, status, Response , HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from login.database import get_db 
from login import schema, model, utility, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login')
# def login(user_credential: schema.UserLogin, db: Session = Depends(get_db)):
#     user = db.query(model.User).filter(model.User.email == user_credential.email).first()

#     if not user:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail= "Invalid Credentials")

#     if not utility.verify(user_credential.password, user.password):
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail= "Invalid Credentials")

#     access_token = oauth2.create_access_token(data={"user_id":user.id})
#     return {"access token": access_token, "token_type":"bearer"}


def login(user_credential:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.email == user_credential.username).first()

    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN , detail= "Invalid Credentials")

    if not utility.verify(user_credential.password, user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN , detail= "Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id":user.id})
    return {"access_token": access_token, "token_type":"bearer"}










