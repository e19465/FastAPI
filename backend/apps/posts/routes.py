from fastapi import APIRouter
from . import models
from database import engine, get_db
from fastapi import status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from .validators import GetPostResponseValidator, CreatePostResponseValidator, UpdatePostValidator, CreatePostValidator, UpdateResponseValidator
##############################################################################################################

##########! configuration ##################
post_router = APIRouter(
    prefix="/posts",
    tags=['Post']
)
models.Base.metadata.create_all(bind=engine)








#!########### GET ALL POSTS #########################
@post_router.get("/getAll",status_code=status.HTTP_200_OK, response_model=List[GetPostResponseValidator])
def get_all_posts(db: Session = Depends(get_db)):
    """
    # Retrieve all posts.

    **Response:**

        List of all posts.
    """
    try:
        all_posts = db.query(models.Post).all()
        return  all_posts
    except Exception as e: 
        return {"error": str(e)}



#!########### CREATE NEW POST ########################
@post_router.post("/create", response_model=CreatePostResponseValidator, status_code=status.HTTP_201_CREATED)
async def create_post(new_post: CreatePostValidator, db: Session = Depends(get_db)):
    """
    # Create a new post.

    **Args:**

        new_post (CreatePostValidator): Data for creating a new post.

    **Response:**

        CreatePostResponseValidator: Details of the newly created post.
    """
    try:
        new_post.model_dump()
        post = models.Post(**new_post.model_dump())
        db.add(post)
        db.commit()
        return post
    except Exception as e:
        return {"error": str(e)}

 
#!########### GET ONE POST #########################
@post_router.get("/single/{post_id}", response_model=GetPostResponseValidator, status_code=status.HTTP_200_OK)
async def get_one_post(post_id:str, db: Session = Depends(get_db)):
    """
    # Retrieve a single post by its ID.

    **Args:**

        post_id (str): The ID of the post to retrieve.

    **Response:**

        Details of the requested post.
    """
    try:
        one_post = db.query(models.Post).filter(models.Post.id == post_id).first()
        if not one_post:
            return JSONResponse({"error":f"Post with id {post_id} not found"}, status_code=status.HTTP_404_NOT_FOUND)
        return one_post
    except Exception as e:
        return {"error": str(e)}


#!########### UPDATE ONE POST #######################
@post_router.patch("/update/{post_id}", response_model=UpdateResponseValidator, status_code=status.HTTP_200_OK)
async def update_post(post_id:str, post: UpdatePostValidator,  db: Session = Depends(get_db)):
    """
    # Update a post by its ID.

    **Args:**

        - post_id (str): The ID of the post to update.
        - post: Data for updating the post.

    Returns:
        UpdateResponseValidator: Details of the updated post.
    """
    try:
        post_query = db.query(models.Post).filter(models.Post.id == post_id)
        if not post_query.first():
            return JSONResponse({"error":f"Post with id {post_id} not found"}, status_code=status.HTTP_404_NOT_FOUND)

        post_query.update(post.model_dump(), synchronize_session=False)
        db.commit()

        updated_post = post_query.first()
        return updated_post
    except Exception as e:
        return {"ERROR": str(e)}



#!########### DELETE ONE POST #########################
@post_router.delete("/delete/{post_id}")
async def delete_post(post_id: str, db: Session = Depends(get_db)):
    """
    # Delete a post by its ID.

    **Args:**

        post_id (str): The ID of the post to delete.
    
    **Returns:**

        JSONResponse: Confirmation message upon successful deletion.
    """
    try:
        deleted_post_query = db.query(models.Post).filter(models.Post.id == post_id)
        if not deleted_post_query.first():
            return JSONResponse({"error":f"Post with id {post_id} not found"}, status_code=status.HTTP_404_NOT_FOUND)
        else:
            deleted_post_query.delete(synchronize_session=False)
            db.commit()
            return JSONResponse({"message": "post has been deleted successfully"}, status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        print(e)
        return JSONResponse({"Error": "An error has occured during deleting process"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

