from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routes.users import user_router
from routes.likes import likes_router
from routes.posts import post_router
from routes.common.logout import logout_router
from routes.tokens import refresh_router
from fastapi.middleware.cors import CORSMiddleware
from middleware import cors_settings
import models
from database import engine

#
#!# end imports #######################


models.Base.metadata.create_all(bind=engine)

#!# configurations start ##############
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


#! adding middleware
app.add_middleware(
    CORSMiddleware,
    **cors_settings
)


#! index route
@app.get("/")
async def get_index():
    return FileResponse("static/index.html")


#! routing configurations #####
app.include_router(post_router)
app.include_router(user_router)
app.include_router(logout_router)
app.include_router(refresh_router)
app.include_router(likes_router)

#! 404 page


@app.get("/{path}", status_code=404)
async def not_found(request: Request, path: str):
    return FileResponse("static/404.html")
