from typing import List

from fastapi import APIRouter, Body, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder


from app.models.config import (
    Config,
    ConfigUpdate,
)


router = APIRouter()


CONFIG_TABLE_NAME = "configs"


@router.post(
    "/",
    response_description="Create a new config",
    status_code=status.HTTP_201_CREATED,
    response_model=Config,
)
def create_config(request: Request, config: Config = Body(...)):
    conf = jsonable_encoder(config)
    new_config = request.app.database[CONFIG_TABLE_NAME].insert_one(conf)
    created_config = request.app.database[CONFIG_TABLE_NAME].find_one(
        {"_id": new_config.inserted_id}
    )

    return created_config


@router.get(
    "/", response_description="List configs", response_model=List[Config]
)
def list_configs(request: Request, limit: int = 1000):
    configs = list(request.app.database[CONFIG_TABLE_NAME].find())
    configs.sort(key=lambda r: r["updated_at"], reverse=True)
    return configs[:limit]


@router.get(
    "/{id}",
    response_description="Get a single config by id",
    response_model=Config,
)
def find_config(id: str, request: Request):
    if (
        config := request.app.database[CONFIG_TABLE_NAME].find_one({"_id": id})
    ) is not None:
        return config

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Config with ID {id} not found",
    )


@router.put(
    "/{id}", response_description="Update a config", response_model=Config
)
def update_config(id: str, request: Request, config: ConfigUpdate = Body(...)):
    config = {k: v for k, v in config.dict().items() if v is not None}
    if len(config) >= 1:
        update_result = request.app.database[CONFIG_TABLE_NAME].update_one(
            {"_id": id}, {"$set": config}
        )
        if update_result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Config with ID {id} not found",
            )
    if (
        existing_config := request.app.database[CONFIG_TABLE_NAME].find_one(
            {"_id": id}
        )
    ) is not None:
        return existing_config

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Config with ID {id} not found",
    )
