from fastapi import FastAPI
from apps.posts.routes import post_router
from apps.users.routes import user_router
#!################### end imports ###########################################


#!################### configurations start ###################################
app = FastAPI()




#######################! routing configurations ##############################
app.include_router(post_router)
app.include_router(user_router)







