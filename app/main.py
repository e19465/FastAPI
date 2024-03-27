import os
import time
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from fastapi import  FastAPI, status, Request, Response, Depends
from fastapi.responses import Response
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
import models
from database import engine, get_db
from sqlalchemy.orm import Session

#!################### configurations start ###################################
load_dotenv()
app = FastAPI()
models.Base.metadata.create_all(bind=engine)



# connection to database
while(True):
    try: 
        connection = psycopg2.connect(
            host=os.environ.get('DATABASE_HOST'),
            database=os.environ.get('DATABASE_NAME'),
            user=os.environ.get('DATABASE_USER'),
            password=os.environ.get('DATABASE_PASSWORD'),
            cursor_factory=RealDictCursor
            )
        cursor = connection.cursor()
        print("Database connection was successfull.")
        break
    except Exception as e:
        print("Database connection failed.")
        print("Error: ", e)
        time.sleep(2)
#!################### configurations end ###################################

class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get("/sql")
def test_get(db: Session = Depends(get_db)):
    return {"data":"success"}

@app.get("/posts/getAll")
def get_all_posts():
    try:
        cursor.execute("""SELECT * FROM posts""")
        posts = cursor.fetchall()
        return {"data": posts}
    except Exception as e:
        # Handle the exception
        return {"error": str(e)}


@app.post("/create/post")
async def create_post(new_post: Post, request: Request, response: Response):
    try:
        post_id = uuid4()  # Generate a new UUID for the post
        str_post_id = str(post_id)  # Convert UUID to string
        post_title = new_post.title
        post_content = new_post.content
        post_published = new_post.published

        cursor.execute(
            """
            INSERT INTO posts (id, title, content, published)
            VALUES (%s, %s, %s, %s) RETURNING *
            """,
            (str_post_id, post_title, post_content, post_published)
        )
        new_post = cursor.fetchone()
        connection.commit()
        return Response(status_code=status.HTTP_201_CREATED)
    except Exception as e:
        # Handle the exception
        return {"error": str(e)}

 

@app.get("/posts/getOne/{id}")
async def get_one_post(request: Request):
    try:
        post_id = request.path_params.get('id')
        cursor.execute("""SELECT * FROM posts WHERE id=%s""", (post_id,))
        one_post = cursor.fetchone()

        if not one_post:
            raise HTTPException(detail=f"Post with id {post_id} not found", status_code=status.HTTP_404_NOT_FOUND)

        return Response(status_code=status.HTTP_200_OK)
    except Exception as e:
        # Handle the exception
        return {"error": str(e)}

@app.patch("/posts/update/{id}")
async def update_post(request: Request):
    print(request.body)
    try:
        post_id = request.path_params.get('id')
        data = await request.json()
        title = data["title"]
        content = data["content"]
        published = data["published"]
        cursor.execute(
            """UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""", 
            (title, content, published, post_id)
        )

        edited_post = cursor.fetchone()
        connection.commit()

        return {"data": edited_post}
    except Exception as e:
        return {"ERROR": str(e)}


@app.delete("/posts/delete/{id}")
async def delete_post(request: Request):
    try:
        post_id = request.path_params.get('id')
        cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (post_id,))
        deleted_post = cursor.fetchone()
        if not deleted_post:
            raise HTTPException(detail=f"Post with id {post_id} not found", status_code=status.HTTP_404_NOT_FOUND)
        connection.commit()
        return {"data": deleted_post}
    except Exception as e:
        # Handle the exception
        return Response(status_code=status.HTTP_204_NO_CONTENT)