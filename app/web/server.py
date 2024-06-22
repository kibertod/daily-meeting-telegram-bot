from fastapi import FastAPI
from .router import setup_router
import uvicorn


def main():
    app = FastAPI()
    setup_router(app)
    uvicorn.run(app, host="0.0.0.0", port=7050)

