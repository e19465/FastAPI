import os
import json
import jwt
from database import engine, get_db
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import status, APIRouter, Request, Depends
from . import models
from .validators import CreateLikeValidator
from auth.verifyTokens import verify_access_token
from auth.getTokens import get_access_token, get_refresh_token
from apps.posts.models import Post

#! configuration ########
likes_router = APIRouter(
    prefix="/likes",
    tags=['Likes']
)
models.Base.metadata.create_all(bind=engine)
#! end configuration ####


#! IF YOUR DATABASE HAS NOT THIS TABLE, JUST RUN THIS END POINT ##
@likes_router.get("/create_table", status_code=status.HTTP_200_OK)
def create_table():
    return {"message":"table is created"}

@likes_router.post("/like", status_code=status.HTTP_201_CREATED)
async def add_like(like: CreateLikeValidator, request: Request, db: Session = Depends(get_db)):
    user_id = verify_access_token(request)

    # if extracted user id is a JSON error response instead of actual user id, immediately return it
    if isinstance(user_id, JSONResponse):
        return user_id
    
    found_post = db.query(Post).filter(Post.id == like.post_id).first()

    if not found_post:
        return JSONResponse({"error":"post not found"}, status_code=status.HTTP_404_NOT_FOUND)
    
    like_query = db.query(models.Likes).filter(models.Likes.post_id == like.post_id, models.Likes.user_id == user_id)
    found_like = like_query.first()
        

    if (like.direction):
        if found_like:
            return JSONResponse({"message":"you already liked this post"}, status_code=status.HTTP_409_CONFLICT)
        else:
            new_like = models.Likes(post_id=like.post_id, user_id=user_id)
            db.add(new_like)
            db.commit()
            return {"message":"Like added successfully"}
    else:
        if not found_like:
            return JSONResponse({"message":"you are not liked this post yet"}, status_code=status.HTTP_404_NOT_FOUND)
        else:
            like_query.delete(synchronize_session=False)
            db.commit()
            return {"message":"Like removed successfully"}
    

    


