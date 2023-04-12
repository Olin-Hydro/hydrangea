import os

from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_html
from pymongo import MongoClient
from app.routes.garden import router as garden_router
from app.routes.sensor import router as sensor_router
from app.routes.scheduled_actuator import router as scheduled_actuator_router
from app.routes.reactive_actuator import router as reactive_actuator_router
from app.routes.command import router as command_router
from app.routes.config import router as config_router
from app.routes.logging import router as logging_router
from dotenv import load_dotenv
from mangum import Mangum


load_dotenv()

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


@app.get("/docs", include_in_schema=False)
def custom_swagger_ui_html(req: Request):
    root_path = req.scope.get("root_path", "").rstrip("/")
    openapi_url = root_path + app.openapi_url
    return get_swagger_ui_html(
        openapi_url=openapi_url,
        title="API",
    )


app.include_router(garden_router, tags=["gardens"], prefix="/garden")
app.include_router(sensor_router, tags=["sensors"], prefix="/sensor")
app.include_router(
    scheduled_actuator_router, tags=["scheduled_actuators"], prefix="/sa"
)
app.include_router(reactive_actuator_router, tags=["reactive_actuators"], prefix="/ra")
app.include_router(command_router, tags=["commands"], prefix="/cmd")
app.include_router(logging_router, tags=["logging"])
app.include_router(config_router, tags=["configs"], prefix="/config")


handler = Mangum(app)
