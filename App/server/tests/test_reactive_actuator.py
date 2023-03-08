import os
import sys

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

parent = os.path.abspath(".")
sys.path.append(parent)
sys.path.append("../server")

from App.server.routes.reactive_actuator import router as ra_router

app = FastAPI()
app.include_router(ra_router, tags=["reactive_actuator"], prefix="/ra")


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
    app.database.drop_collection("reactive_actuators")


def test_create_ra():
    with TestClient(app) as client:
        response = client.post(
            "/ra/", json={"name": "Don Quixote", "sensor_id": "a47a4b121"}
        )
        assert response.status_code == 201
        body = response.json()
        assert body.get("name") == "Don Quixote"
        assert body.get("sensor_id") == "a47a4b121"
        assert "_id" in body


def test_create_ra_missing_name():
    with TestClient(app) as client:
        response = client.post("/ra/", json={"sensor_id": "a47a4b121"})
        assert response.status_code == 422


def test_create_ra_missing_sensor_id():
    with TestClient(app) as client:
        response = client.post("/ra/", json={"name": "Don Quixote"})
        assert response.status_code == 422


def test_get_ra():
    with TestClient(app) as client:
        new_ra = client.post(
            "/ra/", json={"name": "Don Quixote", "sensor_id": "a47a4b121"}
        ).json()
        get_ra_response = client.get("/ra/" + new_ra.get("_id"))
        assert get_ra_response.status_code == 200
        assert get_ra_response.json() == new_ra


def test_get_ra_unexisting():
    with TestClient(app) as client:
        get_ra_response = client.get("/ra/unexisting_id")
        assert get_ra_response.status_code == 404


def test_update_ra():
    with TestClient(app) as client:
        new_ra = client.post(
            "/ra/", json={"name": "Don Quixote", "sensor_id": "a47a4b121"}
        ).json()

        response = client.put(
            "/ra/" + new_ra.get("_id"), json={"name": "Don Quixote 1"}
        )
        assert response.status_code == 200
        assert response.json().get("name") == "Don Quixote 1"


def test_update_ra_unexisting():
    with TestClient(app) as client:
        update_ra_response = client.put(
            "/ra/unexisting_id", json={"name": "Don Quixote 1"}
        )
        assert update_ra_response.status_code == 404
