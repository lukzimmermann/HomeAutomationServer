from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers.hue.hue import router as hue_router

description = """
😎 
"""

app = FastAPI(title="HomeAutomationServer", description=description)
app.include_router(hue_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)