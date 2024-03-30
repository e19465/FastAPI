from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from apps.posts.routes import post_router
from apps.users.routes import user_router
from common.logout import logout_router
from common.refreshTokens import refresh_router

#!################### end imports ###########################################


#!################### configurations start ###################################
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# index route
@app.get("/")
async def get_index():
    return FileResponse("static/index.html")




#######################! routing configurations ##############################
app.include_router(post_router)
app.include_router(user_router)
app.include_router(logout_router)
app.include_router(refresh_router)





#404 page
@app.get("/{path}", status_code=404)
async def not_found(request: Request, path: str):
    return FileResponse("static/404.html")

