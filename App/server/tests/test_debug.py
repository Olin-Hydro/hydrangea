from datetime import datetime
import os
import sys
import json
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


def test_list_sa_logs():
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
            "/sa/logging/actions/" + "?start=" + start + "&end=" + end
        )
        print(new_sa)
        print(new_sa_log)
        body = get_log_response.json()
        print(body)
        result = sorted(body, key=lambda x: x["updated_at"], reverse=False)
        print(result)

        assert get_log_response.status_code == 200
        assert get_log_response.json()[0] == new_sa_log


test_list_sa_logs()
