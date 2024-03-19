from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.api.api_router import api_router

app = FastAPI(
    title="Linekdin API",
    description="this is a tool to download the videos, pictures, documents, etc of a Linkedin.com post.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url=None,
)

# config static files and templates
app.mount("/static", StaticFiles(directory="src/static"), name="static")


app.include_router(api_router)
