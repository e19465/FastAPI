## MIDDLEWARE ## 

#! Configure CORS settings
cors_allowed_origins = [
    "http://localhost",
    "http://localhost:8080",
]

cors_allowed_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
cors_allowed_headers = ["*"]


cors_settings = {
    "allow_origins": cors_allowed_origins,
    "allow_credentials": True,
    "allow_methods": cors_allowed_methods,
    "allow_headers": cors_allowed_headers,
}



