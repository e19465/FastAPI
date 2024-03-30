import os
import jwt
from auth.verifyTokens import verify_access_token
from fastapi.responses import JSONResponse
from database import engine, get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, status, Depends, Request
from .. import models
from apps.users.models import User
##########################################################################

#! configuration ######
logout_router = APIRouter()
models.Base.metadata.create_all(bind=engine)
#! end configuration ##

@logout_router.delete("/logout", status_code=status.HTTP_200_OK)
async def logout_fn(request: Request, db: Session = Depends(get_db)):
    """
    # Log out the user by deleting their refresh token from the database.

    **Args:**

        - request header needs to contain access token

    **Response:**
        
        JSONResponse: A JSON response indicating the status of the logout process.
    """
    refresh_secret_key = os.environ.get("REFRESH_TOKEN_SECRET")
    if request.method == 'DELETE':
        userId = verify_access_token(request)
        
        if isinstance(userId, JSONResponse):
            return userId # if error occured during token verification, return error
        

        is_tokens_cleared = await token_clearing(db, userId, refresh_secret_key)

        if is_tokens_cleared:
            return JSONResponse({"message": "Logout successfull"}, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse({"error": "an error occured during logging out. Please try again"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    else:
        return JSONResponse({"message": "Only DELETE requests are allowed for this endpoint!"}, status_code=status.HTTP_405_METHOD_NOT_ALLOWED)


async def token_clearing(db, userId, refresh_secret_key):
    try:
            found_user = db.query(User).filter(User.id == userId).first()

            if found_user:
                all_refresh_tokens = db.query(models.RefreshToken).all()

                if not (all_refresh_tokens):
                    return JSONResponse({"error":"something went wrong! please try again"}, status_code=status.HTTP_404_NOT_FOUND)

                for refreshToken in all_refresh_tokens:
                    refresh_token = refreshToken.token
                    decoded_refresh_token = jwt.decode(refresh_token, refresh_secret_key, algorithms=['HS256'])
                    token_user_id = decoded_refresh_token['user_id']
                    if token_user_id == userId:
                        db.query(models.RefreshToken).filter(models.RefreshToken.token == refresh_token).delete()
                        db.commit()
                
                return True
            else:
                return False
            
    except Exception as e:
        return False