from fastapi import FastAPI

from userfetchapi.api import users_routes

app = FastAPI()

app.include_router(users_routes.router)
