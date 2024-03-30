import os
import jwt
from fastapi.responses import JSONResponse
from fastapi import status



def verify_access_token(request):
    accessTokenSecret = os.environ.get('ACCESS_TOKEN_SECRET')
    auth_header = request.headers.get('Authorization', None)
    
    if auth_header is not None and auth_header.startswith('Bearer '):
        # Extract the token value from the Authorization header
        access_token = auth_header.split(' ')[1]  # Split the header by space and take the second part

        # check database, if access token is available or not
        if not access_token:
            return JSONResponse({"message": "You are not authenticated!"}, status_code=status.HTTP_401_UNAUTHORIZED)
        

        try:
            
            # Verify access token
            decoded_access_token = jwt.decode(access_token, accessTokenSecret, algorithms=['HS256'])
            user_id = decoded_access_token['user_id']
            return user_id
        
        except jwt.ExpiredSignatureError:
            return JSONResponse({"message": "Access token has expired!"}, status_code=status.HTTP_403_FORBIDDEN)
        except jwt.InvalidTokenError:
            return JSONResponse({"message": "Invalid access token!"}, status_code=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            error_message = "An error occurred during the token verification process."
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            
            if isinstance(e, JSONResponse):
                # If the exception is a JsonResponse object, extract the error message and status code
                error_message = e.content.decode('utf-8')  # Extract the error message from JsonResponse
                status_code = e.status_code  # Extract the status code from JsonResponse
            
            # Return the error message as a JsonResponse
            return JSONResponse({"error": error_message}, status_code=status_code)
                
    else:
        # Handle cases where Authorization header is missing or not in the expected format
        return JSONResponse({"message": "Unauthorized"}, status_code=status.HTTP_401_UNAUTHORIZED)