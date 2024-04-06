import os
import json
import jwt
from fastapi import status, APIRouter, Request, Depends
from  . import models
from fastapi.responses import JSONResponse
from database import engine, get_db
from sqlalchemy.orm import Session
from auth.verifyTokens import verify_access_token
from auth.getTokens import get_access_token, get_refresh_token


#! configuration ########
refresh_router = APIRouter(
    prefix="/token",
    tags=['Token']
)
models.Base.metadata.create_all(bind=engine)
#! end configuration ####


# function to refresh the tokens and get new tokens
@refresh_router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_token_fn(request: Request, db: Session = Depends(get_db)):
    """
    # Refresh the access token using the provided refresh token.

    **Args:**

        - token: existing refresh token
        - get from the request body
        - request header needs to contain access token

    **Response:**
    
        JSONResponse: A JSON response containing the new access and refresh tokens.
    """
    if request.method == 'POST':
        user_id = verify_access_token(request)
        
        if isinstance(user_id, JSONResponse):
            return user_id # if error occured during token verification, return error
        
        
        try:
            body_data = await request.json()
            refreshToken = body_data.get('token')
            

            if not refreshToken:
                return JSONResponse({"error": "refrsh token not provided"}, status_code=status.HTTP_400_BAD_REQUEST)
            
            found_refresh_token = db.query(models.RefreshToken).filter(models.RefreshToken.token == refreshToken)
            if not found_refresh_token:
                return JSONResponse({"message": "Refresh token is not valid!"}, status_code=status.HTTP_403_FORBIDDEN)
            
            # Verify refresh token
            try:
                refresh_secret_key = os.environ.get("REFRESH_TOKEN_SECRET")

                decoded_refresh_token = jwt.decode(refreshToken, refresh_secret_key, algorithms=['HS256'])
                
                # Generate new access token
                new_access_token = get_access_token(decoded_refresh_token['user_id'])

                # Generate new refresh token
                new_refresh_token = get_refresh_token(decoded_refresh_token['user_id'])

                # Remove previous refresh token from database
                found_refresh_token.delete()
                db.commit()

                # adding refresh token to database
                latest_refresh = models.RefreshToken(token=new_refresh_token)
                db.add(latest_refresh)
                db.commit()
        
                # Return new tokens
                return JSONResponse({"access": new_access_token, "refresh": new_refresh_token}, status_code=status.HTTP_200_OK)
            except jwt.ExpiredSignatureError:
                return JSONResponse({"error": "Refresh token has expired!"}, status_code=status.HTTP_403_FORBIDDEN)
            except jwt.InvalidTokenError:
                return JSONResponse({"message": "Invalid refresh token!"}, status_code=status.HTTP_403_FORBIDDEN)
            
            
        except Exception as e:
            print(e)
            error_message = "An error occurred during the update process."
            status_code = 500
            
            if isinstance(e, JSONResponse):
                error_message = e.content.decode('utf-8')
                status_code = e.status_code
            return JSONResponse({"error": error_message}, status_code=status_code)

    else:
        return JSONResponse({"message": "Only POST requests are allowed for this endpoint!"}, status_code=status.HTTP_405_METHOD_NOT_ALLOWED)