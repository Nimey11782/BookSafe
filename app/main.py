from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api import events

app=FastAPI()

app.include_router(auth_router)

app.include_router(events.router)

@app.get("/")
def root():
    return {
        "msg":"BookSafe API is runing"
    }