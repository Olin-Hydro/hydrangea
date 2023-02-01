import os
import sys

sys.path.append("../server")

# sys.path.append('..')

# from dotenv import dotenv_values
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pymongo import MongoClient

parent = os.path.abspath(".")
sys.path.append(parent)


print(sys.path)

from App.server.routes.scheduled_actuator import router as sa_router

app = FastAPI()
# config = dotenv_values(".env")
app.include_router(sa_router, tags=["scheduled_actuators"], prefix="/sa")


@app.on_event("startup")
async def startup_event():
    app.mongodb_client = MongoClient(os.environ["ATLAS_URI"])
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
        get_sa_response = client.get("/garden/" + new_sa.get("_id"))
        assert get_sa_response.status_code == 200
        assert get_sa_response.json() == new_sa


def test_get_sa_unexisting():
    with TestClient(app) as client:
        get_garden_response = client.get("/sa/unexisting_id")
        assert get_garden_response.status_code == 404


def test_update_garden():
    with TestClient(app) as client:
        new_sa = client.post(
            "/sa/", json={"name": "Don Quixote", "garden_id": "a47a4b121"}
        ).json()

        response = client.put(
            "/sa/" + new_sa.get("_id"), json={"name": "Don Quixote 1"}
        )
        assert response.status_code == 200
        assert response.json().get("name") == "Don Quixote 1"


def test_update_garden_unexisting():
    with TestClient(app) as client:
        update_sa_response = client.put(
            "/sa/unexisting_id", json={"name": "Don Quixote 1"}
        )
        assert update_sa_response.status_code == 404


def test_delete_garden():
    with TestClient(app) as client:
        new_sa = client.post(
            "/sa/", json={"name": "Don Quixote", "garden_id": "a47a4b121"}
        ).json()

        delete_sa_response = client.delete("/garden/" + new_sa.get("_id"))
        assert delete_sa_response.status_code == 204


def test_delete_sa_unexisting():
    with TestClient(app) as client:
        delete_sa_response = client.delete("/sa/unexisting_id")
        assert delete_sa_response.status_code == 404
