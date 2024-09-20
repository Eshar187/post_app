from fastapi import APIRouter, Depends, status, Response,HTTPException
from login.database import get_db
from sqlalchemy.orm import Session
from login import model, schema, utility



router = APIRouter()

@router.post("/users",status_code= status.HTTP_201_CREATED, response_model= schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):

    # hash the password
    hashed_password = utility.hash(user.password)
    user.password = hashed_password

    new_user = model.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/users/{id}", response_model= schema.UserOut)
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()

    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"user with id: {id} not exist")
    return user
