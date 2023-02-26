import os
import sys
from typing import List

from dotenv import load_dotenv
from fastapi import APIRouter, Body, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

parent = os.path.abspath(".")
sys.path.append(parent)


from OldApp.server.database import db
from OldApp.server.models.config import ConfigModel

load_dotenv()


router = APIRouter()


@router.post("/", response_description="Add new config", response_model=ConfigModel)
async def create_config(config: ConfigModel = Body(...)):
    config = jsonable_encoder(config)
    new_config = await db["configs"].insert_one(config)
    created_config = await db["configs"].find_one({"_id": new_config.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_config)


@router.get(
    "/", response_description="List all configs", response_model=List[ConfigModel]
)
async def list_config():
    config = await db["configs"].find().to_list(1000)
    return config
