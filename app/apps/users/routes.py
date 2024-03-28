from fastapi import APIRouter, status, Depends
from .validators import UserRegisterValidator, UserLoginValidator
from database import engine, get_db
from sqlalchemy.orm import Session
from . import models
from fastapi.responses import JSONResponse
import bcrypt

##########! configuration ##################
user_router = APIRouter()
models.Base.metadata.create_all(bind=engine)



def hash_password(password):
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
    return hashed_pw.decode('utf-8')

def verify_password(password, password_hash):
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
     

    
#!################### LOGIN USER ##########################################################
@user_router.post("/user/login", status_code=status.HTTP_200_OK)
async def login_user(credentials: UserLoginValidator, db: Session = Depends(get_db)):
    try:
        found_user = db.query(models.User).filter(models.User.username == credentials.username).first()

        if not found_user:
            return JSONResponse({"Error":"Wrong Credentials"}, status_code=status.HTTP_400_BAD_REQUEST)

        found_user_password = found_user.password

        is_password_correct = verify_password(credentials.password, found_user_password)
        if not is_password_correct:
            return JSONResponse({"Error":"Wrong Credentials"}, status_code=status.HTTP_400_BAD_REQUEST)
        
        return {"message":"Login Successfull!"}
    
    except Exception as e:
        print(e)
        return JSONResponse({"Error":str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

#!##################### REGISTER USER #################################################
@user_router.post("/user/register", status_code=status.HTTP_201_CREATED)
async def create_user(new_user: UserRegisterValidator, db: Session = Depends(get_db)):
    try:
 
        username_found = db.query(models.User).filter(models.User.username == new_user.username).first()
        email_found = db.query(models.User).filter(models.User.email == new_user.email).first()
        if username_found:
            return JSONResponse({"Error":"Username already exists"}, status_code=status.HTTP_409_CONFLICT)
        
        if email_found:
            return JSONResponse({"Error":"Email already exists"}, status_code=status.HTTP_409_CONFLICT)

        new_user.password = hash_password(new_user.password)
        new_user.model_dump()
        user = models.User(**new_user.model_dump())
        db.add(user)
        db.commit()
        return user
    except Exception as e:
        print(e)
        return JSONResponse({"Error":str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)