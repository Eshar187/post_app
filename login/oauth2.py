from jose import JWTError, jwt
from datetime import datetime, timedelta
from login import schema, model
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from .database import get_db
from sqlalchemy.orm import Session
# from .config import settings



oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY = settings.secret_key
# ALGORITHM = settings.algorithm
# ACESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

SECRET_KEY = "jklhadakljfasoosdkfljasflkjsaflksf_lkfajsdflkjahoief_"
ALGORITHM = "HS256"
ACESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    


# def verify_access_token(token: Annotated[str, Depends(oauth2_schema)]):
def verify_access_token(token: str, credentials_exception):
    
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        id = payload.get("user_id")
        # id = str(id)
        if id is None:
            raise credentials_exception
        token_data = schema.Tokendata(id = id)
 
    except JWTError:
        raise credentials_exception
    
    return token_data


def get_current_user(token: str = Depends(oauth2_schema), db: Session= Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Could not validate", 
                                          headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = db.query(model.User).filter(model.User.id == token.id).first()

    return user








