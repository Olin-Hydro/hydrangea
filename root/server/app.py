import os

from dotenv import load_dotenv

load_dotenv()
import sys

import motor.motor_asyncio
from fastapi import FastAPI

sys.path.append("../server")

from server.routes.garden import router as GardenRouter
from server.routes.sensor import router as SensorRouter

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.college

app.include_router(GardenRouter, tags=["Garden"], prefix="/Garden")

app.include_router(SensorRouter, tags=["Sensor"], prefix="/Sensor")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}