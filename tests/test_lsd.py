from datetime import datetime
import os

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pymongo import MongoClient
from dotenv import load_dotenv
import pytz
from app.routes.sensor import router as sensor_router
from app.routes.garden import router as garden_router
from app.routes.reactive_actuator import router as ra_router
from app.routes.scheduled_actuator import router as sa_router
from app.routes.logging import router as logging_router

# For creating a Pod fixture for testing
from app.models.pod

load_dotenv()

app = FastAPI()

app.include_router(sensor_router, tags=["sensor"], prefix="/sensor")
app.include_router(garden_router, tags=["garden"], prefix="/garden")
app.include_router(ra_router, tags=["reactive_actuator"], prefix="/ra")
app.include_router(sa_router, tags=["scheduled_actuators"], prefix="/sa")
app.include_router(logging_router, tags=["logging"])
ISO8601_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"


@app.on_event("startup")
async def startup_event():
    if os.environ["ATLAS_URI"]:
        app.mongodb_client = MongoClient(os.environ["ATLAS_URI"])
    else:
        app.mongodb_client = MongoClient()
    app.database = app.mongodb_client[os.environ["DB_NAME"] + "test"]


@app.on_event("shutdown")
async def shutdown_event():
    app.mongodb_client.close()
    app.database.drop_collection("gardens")

def test_create_garden_no_location_argument():
    """
    When creating the garden object, a name and location are required. This
    function checks that if a location is not given in the request body, then
    the return status is 422 unprocessable content to signify an error has
    occurred.
    """
    with TestClient(app) as client:
        response = client.post(
            "/garden/",
            json={
                "name": "Don Quixote",
                "config_id": "123",
            },
        )
        assert response.status_code == 422

def test_create_garden_no_name_argument():
    """
    When creating the garden object, a name and location are required. This
    function checks that if a name is not given in the request body, then
    the return status is 422 unprocessable content to signify an error has
    occurred.
    """
    with TestClient(app) as client:
        response = client.post(
            "/garden/",
            json={
                "location": "Miguel de Cervantes",
                "config_id": "123",
            },
        )
        assert response.status_code == 422

def test_create_garden_optional_config_id():
    """
    When creating the garden object, a name and location are required. There
    are also optional arguments such as config_id and pods. This test checks if
    a config_id has been included in the request body, the response will
    contain a parameter "config_id" with value specified by the request.
    """
    with TestClient(app) as client:
        response = client.post(
            "/garden/",
            json={
                "name": "Don Quixote",
                "location": "Miguel de Cervantes",
                "config_id": "123",
            },
        )
        assert response.status_code == 201

        body = response.json()
        assert body.get("name") == "Don Quixote"
        assert body.get("location") == "Miguel de Cervantes"
        assert body.get("config_id") == "123"
        assert "_id" in body

def test_create_garden_optional_pods():
    """
    When creating the garden object, a name and location are required. There
    are also optional arguments such as config_id and pods. This test checks if
    a pods argument has been included in the request body, there is a resopnse
    given by the client.
    """
    with TestClient(app) as client:
        response = client.post(
            "/garden/",
            json={
                "name": "Don Quixote",
                "location": "Miguel de Cervantes",
                "pods": [Pod(
                    {"name" : "Spain",
                     "id" : "321",
                     "location" : [1, 2, 3]}
                )],
            },
        )
        assert response.status_code == 201

        body = response.json()
        assert body.get("name") == "Don Quixote"
        assert body.get("location") == "Miguel de Cervantes"
        assert "_id" in body