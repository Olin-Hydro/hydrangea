from datetime import datetime
import os
import sys

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pymongo import MongoClient
from dotenv import load_dotenv
import pytz

load_dotenv()

parent = os.path.abspath(".")
sys.path.append(parent)
sys.path.append("../server")

from App.server.routes.sensor import router as sensor_router
from App.server.routes.garden import router as garden_router
from App.server.routes.reactive_actuator import router as ra_router
from App.server.routes.scheduled_actuator import router as sa_router
from App.server.routes.logging import router as logging_router

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


def test_create_reading():
    with TestClient(app) as client:
        new_garden = client.post(
            "/garden/",
            json={
                "name": "Don Quixote",
                "location": "Miguel de Cervantes",
                "config_id": "abc",
            },
        ).json()
        new_sensor = client.post(
            "/sensor/",
            json={
                "name": "Humidity",
                "garden_id": new_garden.get("_id"),
            },
        ).json()
        response = client.post(
            "/sensors/logging/", json={"sensor_id": new_sensor.get("_id"), "value": "5"}
        )
        assert response.status_code == 201
        body = response.json()
        assert body.get("sensor_id") == new_sensor.get("_id")
        assert body.get("value") == 5
        assert "_id" in body
        assert "created_at" in body


def test_create_reading_missing_sensor_id():
    with TestClient(app) as client:
        response = client.post("/sensors/logging/", json={"value": "5"})
        assert response.status_code == 422


def test_create_reading_missing_value():
    with TestClient(app) as client:
        new_sensor = client.post(
            "/sensor/",
            json={
                "name": "Humidity",
                "garden_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
            },
        ).json()
        response = client.post(
            "/sensors/logging/", json={"sensor_id": new_sensor.get("_id")}
        )
        assert response.status_code == 422


def test_list_reading():
    with TestClient(app) as client:
        new_garden = client.post(
            "/garden/",
            json={
                "name": "Don Quixote",
                "location": "Miguel de Cervantes",
                "config_id": "abc",
            },
        ).json()
        new_sensor = client.post(
            "/sensor/",
            json={
                "name": "Humidity",
                "garden_id": new_garden.get("_id"),
            },
        ).json()
        new_reading = client.post(
            "/sensors/logging/", json={"sensor_id": new_sensor.get("_id"), "value": "5"}
        ).json()
        start = new_reading.get("created_at")
        end = datetime.now(pytz.timezone("US/Eastern")).strftime(ISO8601_FORMAT)
        get_reading_response = client.get(
            "/sensors/logging/" + "?start=" + start + "&end=" + end
        )
        print(new_garden)
        print(new_sensor)
        print(new_reading)
        print(get_reading_response.json())
        # assert get_reading_response.status_code == 200
        # assert get_reading_response.json()[0] == new_reading


def test_list_reading_invalid_time():
    with TestClient(app) as client:
        get_reading_response = client.get(
            "/sensors/logging/" + "?start=1234" + "&end=5678"
        )
        assert get_reading_response.status_code == 400


def test_find_reading():
    with TestClient(app) as client:
        new_garden = client.post(
            "/garden/",
            json={
                "name": "Don Quixote",
                "location": "Miguel de Cervantes",
                "config_id": "abc",
            },
        ).json()
        new_sensor = client.post(
            "/sensor/",
            json={
                "name": "Humidity",
                "garden_id": new_garden.get("_id"),
            },
        ).json()
        new_reading = client.post(
            "/sensors/logging/", json={"sensor_id": new_sensor.get("_id"), "value": "5"}
        ).json()
        start = new_reading.get("created_at")
        end = datetime.now(pytz.timezone("US/Eastern")).strftime(ISO8601_FORMAT)
        get_reading_response = client.get(
            "/sensors/logging/"
            + new_reading.get("sensor_id")
            + "?start="
            + start
            + "&end="
            + end
        )
        assert get_reading_response.status_code == 200
        assert get_reading_response.json()[0] == new_reading


def test_find_reading_invalid_time():
    with TestClient(app) as client:
        new_sensor = client.post(
            "/sensor/",
            json={
                "id": "123456789",
                "name": "Humidity",
                "garden_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
            },
        ).json()
        new_reading = client.post(
            "/sensors/logging/", json={"sensor_id": new_sensor.get("_id"), "value": "5"}
        ).json()
        get_reading_response = client.get(
            "/sensors/logging/123456789?start=1234&end=5678"
        )
        assert get_reading_response.status_code == 400


def test_find_reading_unexisting():
    with TestClient(app) as client:
        get_reading_response = client.get("/sensors/logging/unexisting_id")
        assert get_reading_response.status_code == 404


def test_create_sa_log():
    with TestClient(app) as client:
        new_sa = client.post(
            "/sa/", json={"name": "Don Quixote", "garden_id": "a47a4b121"}
        ).json()
        response = client.post(
            "/sa/logging/actions/", json={"actuator_id": new_sa.get("_id"), "data": "5"}
        )
        assert response.status_code == 201
        body = response.json()
        assert body.get("actuator_id") == new_sa.get("_id")
        assert body.get("data") == "5"
        assert "_id" in body
        assert "created_at" in body


def test_create_sa_log_missing_actuator_id():
    with TestClient(app) as client:
        response = client.post("/sa/logging/actions/", json={"data": "5"})
        assert response.status_code == 422


def test_create_sa_log_missing_data():
    with TestClient(app) as client:
        new_sa = client.post(
            "/sa/", json={"name": "Don Quixote", "garden_id": "a47a4b121"}
        ).json()
        response = client.post(
            "/sa/logging/actions/", json={"actuator_id": new_sa.get("_id")}
        )
        assert response.status_code == 422


def test_create_sa_log_unexisting_actuator_id():
    with TestClient(app) as client:
        response = client.post(
            "/sa/logging/actions/", json={"actuator_id": "123", "data": "5"}
        )
        assert response.status_code == 404


def test_list_sa_logs():
    app.database.drop_collection("scheduled_actions")
    with TestClient(app) as client:
        new_sa = client.post(
            "/sa/", json={"name": "Don Quixote", "garden_id": "a47a4b121"}
        ).json()
        new_sa_log = client.post(
            "/sa/logging/actions/", json={"actuator_id": new_sa.get("_id"), "data": "5"}
        ).json()
        start = new_sa_log.get("created_at")
        end = datetime.now(pytz.timezone("US/Eastern")).strftime(ISO8601_FORMAT)
        get_log_response = client.get(
            "/sa/logging/actions/?limit=1&start=" + start + "&end=" + end
        )
        assert get_log_response.status_code == 200
        result = sorted(
            get_log_response.json(), key=lambda x: x["updated_at"], reverse=True
        )
        assert result[0] == new_sa_log


def test_list_sa_log_invalid_time():
    with TestClient(app) as client:
        get_log_response = client.get(
            "/sa/logging/actions/" + "?start=1234" + "&end=5678"
        )
        assert get_log_response.status_code == 400


def test_find_sa_logs():
    with TestClient(app) as client:
        new_sa = client.post(
            "/sa/", json={"name": "Don Quixote", "garden_id": "a47a4b121"}
        ).json()
        new_sa_log = client.post(
            "/sa/logging/actions/", json={"actuator_id": new_sa.get("_id"), "data": "5"}
        ).json()
        start = new_sa_log.get("created_at")
        end = datetime.now(pytz.timezone("US/Eastern")).strftime(ISO8601_FORMAT)
        get_log_response = client.get(
            "/sa/logging/actions/"
            + new_sa_log.get("actuator_id")
            + "?start="
            + start
            + "&end="
            + end
        )
        assert get_log_response.status_code == 200
        assert get_log_response.json()[0] == new_sa_log


def test_find_sa_log_unexisting():
    with TestClient(app) as client:
        get_log_response = client.get("/sa/logging/actions/unexisting_id")
        assert get_log_response.status_code == 404


def test_find_sa_log_invalid_time():
    with TestClient(app) as client:
        new_sa = client.post(
            "/sa/",
            json={"name": "Don Quixote", "garden_id": "a47a4b121"},
        ).json()
        client.post(
            "/sa/logging/actions/", json={"actuator_id": new_sa.get("_id"), "data": "5"}
        )
        get_log_response = client.get(
            "/sa/logging/actions/" + new_sa.get("_id") + "?start=1234&end=5678"
        )
        assert get_log_response.status_code == 400


def test_create_ra_log():
    with TestClient(app) as client:
        new_ra = client.post(
            "/ra/", json={"name": "Don Quixote", "sensor_id": "a47a4b121"}
        ).json()
        response = client.post(
            "/ra/logging/actions/",
            json={"actuator_id": new_ra.get("_id"), "data": "on"},
        )
        assert response.status_code == 201
        body = response.json()
        assert body.get("actuator_id") == new_ra.get("_id")
        assert body.get("data") == "on"
        assert "_id" in body
        assert "created_at" in body


def test_create_ra_log_missing_actuator_id():
    with TestClient(app) as client:
        response = client.post("/ra/logging/actions/", json={"data": "on"})
        assert response.status_code == 422


def test_create_ra_log_missing_data():
    with TestClient(app) as client:
        new_ra = client.post(
            "/ra/", json={"name": "Don Quixote", "sensor_id": "a47a4b121"}
        ).json()
        response = client.post(
            "/ra/logging/actions/", json={"actuator_id": new_ra.get("_id")}
        )
        assert response.status_code == 422


def test_create_ra_log_unexisting_actuator_id():
    with TestClient(app) as client:
        response = client.post(
            "/ra/logging/actions/", json={"actuator_id": "123", "data": "on"}
        )
        assert response.status_code == 404


def test_list_ra_logs():
    app.database.drop_collection("reactive_actions")
    with TestClient(app) as client:
        new_ra = client.post(
            "/ra/", json={"name": "Don Quixote", "sensor_id": "a47a4b121"}
        ).json()
        new_ra_log = client.post(
            "/ra/logging/actions/",
            json={"actuator_id": new_ra.get("_id"), "data": "on"},
        ).json()
        start = new_ra_log.get("created_at")
        end = datetime.now(pytz.timezone("US/Eastern")).strftime(ISO8601_FORMAT)
        get_log_response = client.get(
            "/ra/logging/actions/?start=" + start + "&end=" + end
        )

        assert get_log_response.status_code == 200
        result = sorted(
            get_log_response.json(), key=lambda x: x["updated_at"], reverse=True
        )
        assert result[0] == new_ra_log


def test_list_ra_log_invalid_time():
    with TestClient(app) as client:
        get_log_response = client.get(
            "/ra/logging/actions/" + "?start=1234" + "&end=5678"
        )
        assert get_log_response.status_code == 400


def test_find_ra_logs():
    with TestClient(app) as client:
        new_garden = client.post(
            "/garden/",
            json={
                "name": "Don Quixote",
                "location": "Miguel de Cervantes",
                "config_id": "abc",
            },
        ).json()
        new_sensor = client.post(
            "/sensor/",
            json={
                "name": "Humidity",
                "garden_id": new_garden.get("_id"),
            },
        ).json()
        new_ra = client.post(
            "/ra/",
            json={
                "name": "Don Quixote",
                "sensor_id": new_sensor.get("_id"),
            },
        ).json()
        new_ra_log = client.post(
            "/ra/logging/actions/",
            json={"actuator_id": new_ra.get("_id"), "data": "on"},
        ).json()
        start = new_ra_log.get("created_at")
        end = datetime.now(pytz.timezone("US/Eastern")).strftime(ISO8601_FORMAT)
        get_log_response = client.get(
            "/ra/logging/actions/"
            + new_ra_log.get("actuator_id")
            + "?start="
            + start
            + "&end="
            + end
        )
        assert get_log_response.status_code == 200
        assert get_log_response.json()[0] == new_ra_log


def test_find_ra_log_unexisting():
    with TestClient(app) as client:
        get_log_response = client.get("/ra/logging/actions/unexisting_id")
        assert get_log_response.status_code == 404


def test_find_ra_log_invalid_time():
    with TestClient(app) as client:
        new_garden = client.post(
            "/garden/",
            json={
                "name": "Don Quixote",
                "location": "Miguel de Cervantes",
                "config_id": "abc",
            },
        ).json()
        new_sensor = client.post(
            "/sensor/",
            json={
                "name": "Humidity",
                "garden_id": new_garden.get("_id"),
            },
        ).json()
        new_ra = client.post(
            "/ra/",
            json={
                "name": "Don Quixote",
                "sensor_id": new_sensor.get("_id"),
            },
        ).json()
        new_ra_log = client.post(
            "/ra/logging/actions/",
            json={"actuator_id": new_ra.get("_id"), "data": "on"},
        ).json()
        get_log_response = client.get(
            "/ra/logging/actions/"
            + new_ra_log.get("actuator_id")
            + "?start=1234&end=5678"
        )
        assert get_log_response.status_code == 400
