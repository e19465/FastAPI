import os
import jwt
import time

def get_access_token(user_id):
    TOKEN_EXPIRATION_TIME_MINUTES = 10
    access_secret_key = os.environ.get("ACCESS_TOKEN_SECRET")  # Replace with your actual secret key
    timestamp = time.time()
    expiration_time = timestamp + (TOKEN_EXPIRATION_TIME_MINUTES * 60)
    payload = {
        "user_id": user_id,
        "timestamp": timestamp,
        "exp": expiration_time
    }
    token = jwt.encode(payload, access_secret_key, algorithm="HS256")
    return token



# function to generate the refresh token
def get_refresh_token(user_id):
    TOKEN_EXPIRATION_TIME_MINUTES = 60
    refresh_secret_key = os.environ.get("REFRESH_TOKEN_SECRET")  # Replace with your actual secret key
    timestamp = time.time()
    expiration_time = timestamp + (TOKEN_EXPIRATION_TIME_MINUTES * 60)
    payload = {
        "user_id": user_id,
        "timestamp": timestamp,
        "exp": expiration_time
    }
    token = jwt.encode(payload, refresh_secret_key, algorithm="HS256")
    return token