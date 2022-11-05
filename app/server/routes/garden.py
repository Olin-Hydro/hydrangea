import sys
from dotenv import load_dotenv
from fastapi import APIRouter, Body, status, HTTPException
from fastapi.encoders import jsonable_encoder
from typing import List
from fastapi.responses import JSONResponse, Response
from server.models.garden import GardenModel, UpdateGardenModel
from server.database import db

sys.path.append("../../server")


load_dotenv()


router = APIRouter()


@router.post("/", response_description="Add new garden", response_model=GardenModel)
async def create_garden(garden: GardenModel = Body(...)):
    garden = jsonable_encoder(garden)
    new_garden = await db["gardens"].insert_one(garden)
    created_garden = await db["gardens"].find_one({"_id": new_garden.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_garden)


@router.get(
    "/", response_description="List all gardens", response_model=List[GardenModel]
)
async def list_gardens():
    gardens = await db["gardens"].find().to_list(1000)
    return gardens


@router.get(
    "/{id}", response_description="Get a single garden", response_model=GardenModel
)
async def show_garden(id: str):
    if (garden := await db["gardens"].find_one({"_id": id})) is not None:
        return garden

    raise HTTPException(status_code=404, detail=f"Garden {id} not found")


@router.put("/{id}", response_description="Update a garden", response_model=GardenModel)
async def update_garden(id: str, garden: UpdateGardenModel = Body(...)):
    garden = {k: v for k, v in garden.dict().items() if v is not None}

    if len(garden) >= 1:
        update_result = await db["gardens"].update_one({"_id": id}, {"$set": garden})

        if update_result.modified_count == 1:
            if (
                updated_garden := await db["gardens"].find_one({"_id": id})
            ) is not None:
                return updated_garden

    if (existing_garden := await db["gardens"].find_one({"_id": id})) is not None:
        return existing_garden

    raise HTTPException(status_code=404, detail=f"Garden {id} not found")


@router.delete("/{id}", response_description="Delete a garden")
async def delete_garden(id: str):
    delete_result = await db["gardens"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Garden {id} not found")
