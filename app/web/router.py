from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from . import views

def setup_router(app: FastAPI):
    @app.get("/set_timezone")
    def set_timezone():
        return HTMLResponse(views.set_timezone())
