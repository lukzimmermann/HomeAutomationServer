from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers.hue import hue

description = """
😎
"""

app = FastAPI(title="HomeAutomationServer", description=description)
app.include_router(hue.router)

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1",
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
