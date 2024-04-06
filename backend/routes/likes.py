from database import  get_db
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import status, APIRouter, Request, Depends
import models
from validators.like.request import CreateLikeValidator
from auth.verifyTokens import verify_access_token
from models import Post

#! configuration ########
likes_router = APIRouter(
    prefix="/likes",
    tags=['Likes']
)
#! end configuration ####


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
    

    


