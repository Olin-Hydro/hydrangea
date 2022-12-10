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

from App.server.routes.garden import router as garden_router

app = FastAPI()
# config = dotenv_values(".env")
app.include_router(garden_router, tags=["gardens"], prefix="/garden")


@app.on_event("startup")
async def startup_event():
    app.mongodb_client = MongoClient(os.environ["ATLAS_URI"])
    app.database = app.mongodb_client[os.environ["DB_NAME"] + "test"]


@app.on_event("shutdown")
async def shutdown_event():
    app.mongodb_client.close()
    app.database.drop_collection("gardens")


def test_create_garden():
    with TestClient(app) as client:
        response = client.post(
            "/garden/", json={"name": "Don Quixote", "location": "Miguel de Cervantes"}
        )
        assert response.status_code == 201

        body = response.json()
        assert body.get("name") == "Don Quixote"
        assert body.get("location") == "Miguel de Cervantes"
        assert "_id" in body


def test_create_garden_missing_name():
    with TestClient(app) as client:
        response = client.post("/garden/", json={"location": "Miguel de Cervantes"})
        assert response.status_code == 422


def test_create_garden_missing_location():
    with TestClient(app) as client:
        response = client.post("/garden/", json={"name": "Don Quixote"})
        assert response.status_code == 422


def test_get_garden():
    with TestClient(app) as client:
        new_garden = client.post(
            "/garden/", json={"name": "Don Quixote", "location": "Miguel de Cervantes"}
        ).json()
        get_garden_response = client.get("/garden/" + new_garden.get("_id"))
        assert get_garden_response.status_code == 200
        assert get_garden_response.json() == new_garden


def test_get_garden_unexisting():
    with TestClient(app) as client:
        get_garden_response = client.get("/garden/unexisting_id")
        assert get_garden_response.status_code == 404


def test_update_garden():
    with TestClient(app) as client:
        new_garden = client.post(
            "/garden/", json={"name": "Don Quixote", "location": "Miguel de Cervantes"}
        ).json()

        response = client.put(
            "/garden/" + new_garden.get("_id"), json={"name": "Don Quixote 1"}
        )
        assert response.status_code == 200
        assert response.json().get("name") == "Don Quixote 1"


def test_update_garden_unexisting():
    with TestClient(app) as client:
        update_garden_response = client.put(
            "/garden/unexisting_id", json={"name": "Don Quixote 1"}
        )
        assert update_garden_response.status_code == 404


def test_delete_garden():
    with TestClient(app) as client:
        new_garden = client.post(
            "/garden/", json={"name": "Don Quixote", "location": "Miguel de Cervantes"}
        ).json()

        delete_garden_response = client.delete("/garden/" + new_garden.get("_id"))
        assert delete_garden_response.status_code == 204


def test_delete_garden_unexisting():
    with TestClient(app) as client:
        delete_garden_response = client.delete("/garden/unexisting_id")
        assert delete_garden_response.status_code == 404
