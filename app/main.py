# Importing libraries

import os  # Import the 'os' library for working with environment variables.

from fastapi import FastAPI, Request  # Import necessary FastAPI components.
from fastapi.openapi.docs import get_swagger_ui_html  # Import Swagger UI HTML generator.
from pymongo import MongoClient  # Import the MongoDB client.
from app.routes.garden import router as garden_router  # Import router for garden-related routes.
from app.routes.sensor import router as sensor_router  # Import router for sensor-related routes.
from app.routes.scheduled_actuator import router as scheduled_actuator_router  # Import router for scheduled actuator routes.
from app.routes.reactive_actuator import router as reactive_actuator_router  # Import router for reactive actuator routes.
from app.routes.command import router as command_router  # Import router for command-related routes.
from app.routes.config import router as config_router  # Import router for config-related routes.
from app.routes.logging import router as logging_router  # Import router for logging-related routes.
from dotenv import load_dotenv  # Import the 'load_dotenv' function to load environment variables from a file.
from mangum import Mangum  # Import Mangum for AWS Lambda deployment.


# Loads environment variables from a '.env' file. 
load_dotenv()

# Gets the MongoDB Atlas URI and database name from environment variables.
ATLAS_URI = os.environ["ATLAS_URI"]
DB_NAME = os.environ["DB_NAME"]

# Creates a FastAPI app instance.
app = FastAPI()

# Defines a startup event to initialize the MongoDB client and database.
@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(ATLAS_URI)
    app.database = app.mongodb_client[DB_NAME]

# Define a shutdown event to close the MongoDB client connection when the app is shutdown.
@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

# Create a custom endpoint for Swagger UI documentation.
@app.get("/docs", include_in_schema=False)
def custom_swagger_ui_html(req: Request):
    root_path = req.scope.get("root_path", "").rstrip("/")
    openapi_url = root_path + app.openapi_url
    return get_swagger_ui_html(
        openapi_url=openapi_url,
        title="API",
    )

# Include routers for various API routes.
app.include_router(garden_router, tags=["gardens"], prefix="/garden")
app.include_router(sensor_router, tags=["sensors"], prefix="/sensor")
app.include_router(
    scheduled_actuator_router, tags=["scheduled_actuators"], prefix="/sa"
)
app.include_router(
    reactive_actuator_router, tags=["reactive_actuators"], prefix="/ra"
)
app.include_router(command_router, tags=["commands"], prefix="/cmd")
app.include_router(logging_router, tags=["logging"])
app.include_router(config_router, tags=["configs"], prefix="/config")

# Create a Mangum handler for AWS Lambda deployment.
handler = Mangum(app)
