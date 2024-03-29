import os

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pymongo import MongoClient
from dotenv import load_dotenv
from app.routes.scheduled_actuator import router as sa_router

load_dotenv()

app = FastAPI()
app.include_router(sa_router, tags=["scheduled_actuators"], prefix="/sa")


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
    app.database.drop_collection("scheduled_actuators")


def test_create_sa():
    with TestClient(app) as client:
        response = client.post(
            "/sa/", json={"name": "Don Quixote", "garden_id": "a47a4b121"}
        )
        assert response.status_code == 201
        body = response.json()
        assert body.get("name") == "Don Quixote"
        assert body.get("garden_id") == "a47a4b121"
        assert "_id" in body


def test_create_sa_missing_name():
    with TestClient(app) as client:
        response = client.post("/sa/", json={"garden_id": "a47a4b121"})
        assert response.status_code == 422


def test_create_sa_missing_garden_id():
    with TestClient(app) as client:
        response = client.post("/sa/", json={"name": "Don Quixote"})
        assert response.status_code == 422


def test_get_sa():
    with TestClient(app) as client:
        new_sa = client.post(
            "/sa/", json={"name": "Don Quixote", "garden_id": "a47a4b121"}
        ).json()
        get_sa_response = client.get("/sa/" + new_sa.get("_id"))
        assert get_sa_response.status_code == 200
        assert get_sa_response.json() == new_sa


def test_get_sa_unexisting():
    with TestClient(app) as client:
        get_sa_response = client.get("/sa/unexisting_id")
        assert get_sa_response.status_code == 404


def test_update_sa():
    with TestClient(app) as client:
        new_sa = client.post(
            "/sa/", json={"name": "Don Quixote", "garden_id": "a47a4b121"}
        ).json()

        response = client.put(
            "/sa/" + new_sa.get("_id"), json={"name": "Don Quixote 1"}
        )
        assert response.status_code == 200
        assert response.json().get("name") == "Don Quixote 1"


def test_update_sa_unexisting():
    with TestClient(app) as client:
        update_sa_response = client.put(
            "/sa/unexisting_id", json={"name": "Don Quixote 1"}
        )
        assert update_sa_response.status_code == 404
