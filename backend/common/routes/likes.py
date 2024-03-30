import os
import json
import jwt
from database import engine, get_db
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import status, APIRouter, Request, Depends
from .. import models
from auth.verifyTokens import verify_access_token
from auth.getTokens import get_access_token, get_refresh_token


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
