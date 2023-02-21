import os
import sys


# sys.path.append('..')

# from dotenv import dotenv_values
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

parent = os.path.abspath(".")
sys.path.append(parent)
sys.path.append("../server")


print(sys.path)

from App.server.routes.sensor import router as sensor_router
from App.server.routes.garden import router as garden_router

app = FastAPI()
# config = dotenv_values(".env")
app.include_router(sensor_router, tags=["sensor"], prefix="/sensor")
app.include_router(garden_router, tags=["garden"], prefix="/garden")


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
    app.database.drop_collection("sensors")


def test_create_sensor():
    with TestClient(app) as client:
        client.post(
            "/garden/",
            json={
                "id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "Don Quixote",
                "location": "Miguel de Cervantes",
                "config_id": "abc",
            },
        )

        response = client.post(
            "/sensor/",
            json={
                "name": "Humidity",
                "garden_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
            },
        )

        print(response.status_code)
        assert response.status_code == 201
        body = response.json()
        print(body)
        assert body.get("name") == "Humidity"
        assert body.get("garden_id") == "066de609-b04a-4b30-b46c-32537c7f1f6e"
        assert "_id" in body


def test_create_sensor_missing_name():
    with TestClient(app) as client:
        response = client.post(
            "/sensor/", json={"garden_id": "066de609-b04a-4b30-b46c-32537c7f1f6e"}
        )
        assert response.status_code == 422


def test_create_sensor_missing_garden_id():
    with TestClient(app) as client:
        response = client.post("/sensor/", json={"name": "Humidity"})
        assert response.status_code == 422


def test_create_sensor_unexisting_garden_id():
    with TestClient(app) as client:
        response = client.post(
            "/sensor/",
            json={
                "name": "Humidity",
                "garden_id": "602d755d-a4dc-4bf7-bb1e-4e244b1f9b10",
            },
        )
        assert response.status_code == 404


def test_get_sensor():
    with TestClient(app) as client:
        new_sensor = client.post(
            "/sensor/",
            json={
                "name": "Humidity",
                "garden_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
            },
        ).json()
        get_sensor_response = client.get("/sensor/" + new_sensor.get("_id"))
        assert get_sensor_response.status_code == 200
        assert get_sensor_response.json() == new_sensor


def test_get_sensor_unexisting():
    with TestClient(app) as client:
        get_sensor_response = client.get("/sensor/unexisting_id")
        assert get_sensor_response.status_code == 404


def test_update_sensor():
    with TestClient(app) as client:
        new_sensor = client.post(
            "/sensor/",
            json={
                "name": "Humidity",
                "garden_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
            },
        ).json()

        response = client.put(
            "/sensor/" + new_sensor.get("_id"), json={"name": "Humidity 1"}
        )
        assert response.status_code == 200
        assert response.json().get("name") == "Humidity 1"


def test_update_sensor_unexisting():
    with TestClient(app) as client:
        update_sensor_response = client.put(
            "/sensor/unexisting_id", json={"name": "Humidity 1"}
        )
        assert update_sensor_response.status_code == 404


def test_delete_sensor():
    with TestClient(app) as client:
        new_sensor = client.post(
            "/sensor/",
            json={
                "name": "Humidity",
                "garden_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
            },
        ).json()

        delete_sensor_response = client.delete("/sensor/" + new_sensor.get("_id"))
        assert delete_sensor_response.status_code == 204


def test_delete_sensor_unexisting():
    with TestClient(app) as client:
        delete_sensor_response = client.delete("/sensor/unexisting_id")
        assert delete_sensor_response.status_code == 404
