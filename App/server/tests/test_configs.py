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


from App.server.routes.config import router as config_router

app = FastAPI()
app.include_router(config_router, tags=["configs"], prefix="/config")


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
    app.database.drop_collection("configs")


def test_create_config():
    with TestClient(app) as client:
        response = client.post(
            "/config/",
            json={
                "name": "Config",
                "sensor_schedule": [{"sensor_id": "abc", "interval": 300}],
                "ra_schedule": [
                    {
                        "ra_id": "bcd",
                        "interval": 1200,
                        "threshold": 7.5,
                        "duration": 5,
                        "threshold_type": 0,
                    }
                ],
                "sa_schedule": [
                    {
                        "sa_id": "ccd",
                        "on": [
                            "2023-02-17T08:09:50+0000",
                            "2023-02-17T16:09:50+0000",
                            "2023-02-17T20:09:50+0000",
                        ],
                        "off": [
                            "2023-02-17T08:29:50+0000",
                            "2023-02-17T16:29:50+0000",
                            "2023-02-17T20:29:50+0000",
                        ],
                    }
                ],
            },
        )
        assert response.status_code == 201

        body = response.json()
        assert body.get("name") == "Config"
        assert body.get("sensor_schedule") == [{"sensor_id": "abc", "interval": 300}]
        # TODO: fill in checks here
        assert "_id" in body


def test_create_config_missing_fields():
    with TestClient(app) as client:
        response = client.post("/config/", json={"name": "Config"})
        assert response.status_code == 422


def test_get_config():
    with TestClient(app) as client:
        new_config = client.post(
            "/config/",
            json={
                "name": "Config",
                "sensor_schedule": [{"sensor_id": "abc", "interval": 300}],
                "ra_schedule": [
                    {
                        "ra_id": "bcd",
                        "interval": 1200,
                        "threshold": 7.5,
                        "duration": 5,
                        "threshold_type": 0,
                    }
                ],
                "sa_schedule": [
                    {
                        "sa_id": "ccd",
                        "on": [
                            "2023-02-17T08:09:50+0000",
                            "2023-02-17T16:09:50+0000",
                            "2023-02-17T20:09:50+0000",
                        ],
                        "off": [
                            "2023-02-17T08:29:50+0000",
                            "2023-02-17T16:29:50+0000",
                            "2023-02-17T20:29:50+0000",
                        ],
                    }
                ],
            },
        ).json()
        get_config_response = client.get("/config/" + new_config.get("_id"))
        assert get_config_response.status_code == 200
        assert get_config_response.json() == new_config


def test_get_config_unexisting():
    with TestClient(app) as client:
        get_config_response = client.get("/config/unexisting_id")
        assert get_config_response.status_code == 404


def test_update_config():
    with TestClient(app) as client:
        new_config = client.post(
            "/config/",
            json={
                "name": "Config",
                "sensor_schedule": [{"sensor_id": "abc", "interval": 300}],
                "ra_schedule": [
                    {
                        "ra_id": "bcd",
                        "interval": 1200,
                        "threshold": 7.5,
                        "duration": 5,
                        "threshold_type": 0,
                    }
                ],
                "sa_schedule": [
                    {
                        "sa_id": "ccd",
                        "on": [
                            "2023-02-17T08:09:50+0000",
                            "2023-02-17T16:09:50+0000",
                            "2023-02-17T20:09:50+0000",
                        ],
                        "off": [
                            "2023-02-17T08:29:50+0000",
                            "2023-02-17T16:29:50+0000",
                            "2023-02-17T20:29:50+0000",
                        ],
                    }
                ],
            },
        ).json()
        response = client.put(
            "/config/" + new_config.get("_id"),
            json={"sensor_schedule": [{"sensor_id": "abc", "interval": 400}]},
        )
        assert response.status_code == 200
        assert response.json().get("sensor_schedule") == [
            {"sensor_id": "abc", "interval": 400}
        ]
