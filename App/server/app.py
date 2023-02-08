import os

from fastapi import FastAPI
from pymongo import MongoClient
from server.routes.garden import router as garden_router
from server.routes.sensor import router as sensor_router
from server.routes.scheduled_actuator import router as scheduled_actuator_router


ATLAS_URI = os.environ["ATLAS_URI"]
DB_NAME = os.environ["DB_NAME"]

app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(ATLAS_URI)
    app.database = app.mongodb_client[DB_NAME]


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(garden_router, tags=["gardens"], prefix="/garden")
app.include_router(sensor_router, tags=["sensors"], prefix="/sensor")
app.include_router(
    scheduled_actuator_router, tags=["scheduled actuators"], prefix="/sa"
)
