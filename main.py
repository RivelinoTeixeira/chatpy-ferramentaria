from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from app.routes import router
import os

app = FastAPI(
    title="Chatbot Ferramentaria 4.0 com IA",
    description="Chatbot híbrido (menu + IA) para PowerApps Ferramentaria 4.0",
    version="1.0.0"
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def get_index():
    return FileResponse(os.path.join("app", "index.html"))
