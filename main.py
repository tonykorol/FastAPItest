from fastapi import FastAPI
from app.handlers import auth, events

app = FastAPI()

app.include_router(auth.router, prefix="/api/v1")
app.include_router(events.router, prefix="/api/v1")
