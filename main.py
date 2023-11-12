from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers.hue import hue

description = """
😎
"""

app = FastAPI(title="HomeAutomationServer", description=description)
app.include_router(hue.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.1.130:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
