from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
#! end imports



#! connect to FastAPI
app = FastAPI()


#! Configure CORS settings
allowed_origins = [
    "http://localhost",
    "http://localhost:8080",
]

#! adding middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

#! Custom middleware to check origin
@app.middleware("http")
async def check_origin(request: Request, call_next):
    origin = request.headers.get("Origin")
    if origin not in allowed_origins:
        # If request origin is not allowed, return custom error response
        error_message = {"detail": f"Origin '{origin}' not allowed"}
        return JSONResponse(content=error_message, status_code=403)

    response = await call_next(request)
    return response


