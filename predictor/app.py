from fastapi import FastAPI
from predictor.routers import router

app = FastAPI()

app.include_router(router)
