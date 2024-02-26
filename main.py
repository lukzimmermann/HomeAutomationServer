from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.utils.sensor.sensor_handler import SensorHandler
from src.routers.hue.hue import router as hue_router
from src.routers.sensor.sensor import router as sensor_router

description = """
😎 
"""

app = FastAPI(title="HomeAutomationServer", description=description)
app.include_router(hue_router)
app.include_router(sensor_router)

sensor_handler = SensorHandler()


#@app.on_event("startup")
#async def startup():
#    sensor_handler.start()
#
#@app.on_event("shutdown")
#async def shutdown():
#    sensor_handler.stop()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)