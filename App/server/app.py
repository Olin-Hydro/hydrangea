import os

# from dotenv import dotenv_values
from fastapi import FastAPI
from pymongo import MongoClient
from server.routes.garden import router as garden_router

# import sys


# parent = os.path.abspath(".")
# sys.path.append(parent)

ATLAS_URI = os.environ["ATLAS_URI"]
DB_NAME = os.environ["DB_NAME"]
# config = dotenv_values(".env")

app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(ATLAS_URI)
    app.database = app.mongodb_client[DB_NAME]


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(garden_router, tags=["gardens"], prefix="/garden")
