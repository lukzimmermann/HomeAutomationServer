from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers.hue import hue

description = """
First Deployment with k3s and GitHub action😎
"""

app = FastAPI(title="HomeAutomationServer", description=description)
app.include_router(hue.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)