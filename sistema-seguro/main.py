from fastapi import FastAPI
from utils.db import Base, engine
from utils import models
from routers.subjects import router as subjects_router
from routers.users import router as users_router

from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI(
    
    title = "Sistema de Notas",
    version = "0.1",
    description = "API para la gestion de notas de estudiantes"

)

Base.metadata.create_all(bind = engine)

app.include_router(users_router)
app.include_router(subjects_router)

app.add_middleware(

    CORSMiddleware,
    allow_origins = ["http://localhost:8100"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@app.get("/")
def root():
    return {"message": "Bienvenido al Sistema de Notas API"}

@app.get("/health")
def health():
    return {"status": "ok"}