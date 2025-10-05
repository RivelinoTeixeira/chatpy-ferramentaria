from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.router import router
import uvicorn

app = FastAPI(title="Chatbot Ferramentaria 4.0")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)