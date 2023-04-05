import os

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pymongo import MongoClient
from dotenv import load_dotenv
from app.routes.command import router as command_router

load_dotenv()


app = FastAPI()
app.include_router(command_router, tags=["commands"], prefix="/cmd")


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
    app.database.drop_collection("commands")


def test_create_command():
    with TestClient(app) as client:
        response = client.post(
            "/cmd/",
            json=[
                {
                    "ref_id": "btnrj",
                    "cmd": 1,
                    "type": "reactive actuator",
                    "garden_id": "abc",
                }
            ],
        )
        assert response.status_code == 201

        body = response.json()[0]
        assert body.get("cmd") == 1
        assert body.get("type") == "reactive actuator"
        assert body.get("garden_id") == "abc"
        assert "_id" in body


def test_create_command_missing_field():
    with TestClient(app) as client:
        response = client.post("/cmd/", json={"cmd": 1})
        assert response.status_code == 422


def test_get_cmd():
    with TestClient(app) as client:
        new_cmd = client.post(
            "/cmd/",
            json=[
                {
                    "ref_id": "hsdjfsk",
                    "cmd": 1,
                    "type": "reactive actuator",
                    "garden_id": "abc",
                }
            ],
        ).json()[0]
        get_cmd_response = client.get("/cmd/" + new_cmd.get("_id"))
        assert get_cmd_response.status_code == 200
        assert get_cmd_response.json() == new_cmd


def test_get_cmd_unexisting():
    with TestClient(app) as client:
        get_cmd_response = client.get("/cmd/unexisting_id")
        assert get_cmd_response.status_code == 404
