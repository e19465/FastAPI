import models
from models import RefreshToken
import os
import bcrypt
from database import get_db
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import APIRouter, status, Depends, Request
from auth.getTokens import get_access_token, get_refresh_token
from auth.verifyTokens import verify_access_token
from routes.common.logout import token_clearing
from validators.user.request import UserRegisterValidator, UserLoginValidator, UserAccountUpdateValidator,UpdateddUserValidator

##########! configuration ##################
user_router = APIRouter(
    prefix="/user",
    tags=['User']
)



#! password hashing and verifying ##########
def hash_password(password):
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
    return hashed_pw.decode('utf-8')

def verify_password(password, password_hash):
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
     
#!##################### REGISTER USER #################################################
@user_router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(new_user: UserRegisterValidator, db: Session = Depends(get_db)):
    """
    # Create a new user account.

    **Response:**

        dict: User details if registration is successful.
    """
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
        return {"message":"Registration Successfull"}
    except Exception as e:
        print(e)
        return JSONResponse({"Error":str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#!################### LOGIN USER #######################################################
@user_router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(credentials: UserLoginValidator, db: Session = Depends(get_db)):
    """
    # Authenticate user credentials and generate access and refresh tokens.

    **Response:**

        dict: Access and refresh tokens.
    """
    try:
        found_user = db.query(models.User).filter(models.User.username == credentials.username).first()

        if not found_user:
            return JSONResponse({"Error":"Wrong Credentials"}, status_code=status.HTTP_400_BAD_REQUEST)


        is_password_correct = verify_password(credentials.password, found_user.password)
        if not is_password_correct:
            return JSONResponse({"Error":"Wrong Credentials"}, status_code=status.HTTP_400_BAD_REQUEST)
        

        access_token = get_access_token(str(found_user.id))
        refresh_token = get_refresh_token(str(found_user.id))
        
        # Create a new RefreshToken instance and assign the token value
        new_refresh_token = RefreshToken(token=refresh_token)
        
        # Add the new RefreshToken to the session
        db.add(new_refresh_token)
        db.commit()


        return {"access": access_token, "refresh": refresh_token}
    
    except Exception as e:
        print(e)
        return JSONResponse({"Error":str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

#!################## ACCOUNT UPDATE ####################################################
@user_router.patch("/account/update",response_model=UpdateddUserValidator ,status_code=status.HTTP_200_OK)
async def update_user(update_data: UserAccountUpdateValidator,request:Request, db: Session = Depends(get_db)):

    """
    # Update user account information.

    **Args:**

        update_data: Updated user account information.
        request (Request): Incoming HTTP request object with access token in the request headers.

    **Response:**

        dict: Updated user account details.
    """

    user_id = verify_access_token(request)

    # if user id is error response instead of actual ID, then immediately return that error response
    if isinstance(user_id, JSONResponse):
        return user_id
    
    found_user_query = db.query(models.User).filter(models.User.id == user_id)

    found_user = found_user_query.first()

    # If user is not found, raise an HTTPException with status code 404
    if not found_user:
        return JSONResponse({"error":"user not found"}, status_code=status.HTTP_404_NOT_FOUND)

    # Update user's data with incoming updated data dynamically
    for field, value in update_data.model_dump(exclude_unset=True).items():
        if field == "password":
            hashed_password = hash_password(value)
            setattr(found_user, field, hashed_password)
        else:
            setattr(found_user, field, value)

    db.commit()
    updated_user = found_user_query.first()

    return updated_user

#!################## ACCOUNT DELETE ####################################################
@user_router.delete("/account/delete", status_code=status.HTTP_200_OK)
async def delete_user(request:Request, db: Session = Depends(get_db)):
    """
    # Delete user account.

    **Args:**

        request (Request): Incoming HTTP request object with access token in the request headers.

    **Response:**
    
        dict: Confirmation message upon successful deletion.
    """
    user_id = verify_access_token(request)

    # if user id is error response instead of actual ID, then immediately return that error response
    if isinstance(user_id, JSONResponse):
        return user_id
    
    found_user=db.query(models.User).filter(models.User.id == user_id).first()
     # If user is not found, raise an HTTPException with status code 404
    if not found_user:
        return JSONResponse({"error":"user not found"}, status_code=status.HTTP_404_NOT_FOUND)


    is_tokens_cleared = await token_clearing(db, user_id, os.environ.get("REFRESH_TOKEN_SECRET"))

    if is_tokens_cleared:
        # Delete the user
        db.delete(found_user)

        # Commit the changes to the database
        db.commit()

        return {"message":"user deleted successfully"}
    else:
        return JSONResponse({"error":"an error occured during account deletion. Please try again"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


