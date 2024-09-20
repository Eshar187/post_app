from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from login import model, schema
from login.database import get_db
from login.oauth2 import get_current_user

router = APIRouter(prefix="/posts",tags=['Posts'])

@router.get("/", response_model= List[schema.PostOUT])
def get_posts(db:Session = Depends(get_db), current_user: int = Depends(get_current_user),
               limit : int = 5, skip: int =0, search: Optional[str]=""):
    # print(current_user.email)
    # posts = db.query(model.Post).filter(model.Post.owner_id == current_user.id).limit(limit).all()
    posts = db.query(model.Post).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(model.Post, func.count(model.Vote.post_id).label("votes")).join(
        model.Vote, model.Vote.post_id == model.Post.id, isouter=True).group_by(model.Post.id).filter(
        model. Post. title. contains(search)).limit(limit).offset(skip).all( )
    
    return results 



@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schema.Post)
def create_posts(post: schema.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(get_current_user)):
    try:
        new_post = model.Post(owner_id = current_user.id, **post.dict())
        
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    except Exception as error:
        return ("Error: ", error)


@router.get('/{id}', response_model= schema.PostOUT)
def get_post(id: int, db:Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    
    # post = db.query(model.Post).filter(model.Post.id == id).first()

    post = db.query(model.Post, func.count(model.Vote.post_id).label("votes")).join(
        model.Vote, model.Vote.post_id == model.Post.id, isouter=True).group_by(model.Post.id).filter(
            model.Post.id == id).first()
    

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    return post

@router.delete('/{id}', status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post_query = db.query(model.Post).filter(model.Post.id == id)
    
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model= schema.Post)
def update_post(id:int, updated_post: schema.PostCreate, db: Session = Depends(get_db)
               , current_user: int = Depends(get_current_user)):
    post_query = db.query(model.Post).filter(model.Post.id == id)
    
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    
    post_query.update(updated_post.dict(), synchronize_session= False)

    db.commit()
    
    return post










