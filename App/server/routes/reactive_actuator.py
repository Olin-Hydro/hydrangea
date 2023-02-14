import sys
from typing import List

from fastapi import APIRouter, Body, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder

try:
    from App.server.models.reactive_actuator import Reactive_Actuator, RA_Update
except ModuleNotFoundError:
    sys.path.append("../server")
    from server.models.reactive_actuator import Reactive_Actuator, RA_Update

router = APIRouter()


@router.post(
    "/",
    response_description="Create a new reactive actuator",
    status_code=status.HTTP_201_CREATED,
    response_model=Reactive_Actuator,
)
def create_reactive_actuator(
    request: Request, reactive_actuator: Reactive_Actuator = Body(...)
):
    ra = jsonable_encoder(reactive_actuator)
    new_ra = request.app.database["reactive_actuators"].insert_one(ra)
    created_ra = request.app.database["reactive_actuators"].find_one(
        {"_id": new_ra.inserted_id}
    )

    return created_ra


@router.get(
    "/",
    response_description="List reactive actuators",
    response_model=List[Reactive_Actuator],
)
def list_reactive_actuators(request: Request, limit: int = 1000):
    reactive_actuators = list(request.app.database["reactive_actuators"].find())
    reactive_actuators.sort(key=lambda r: r["updated_at"], reverse=True)

    return reactive_actuators[:limit]


@router.get(
    "/{id}",
    response_description="Get a single reactive actuator by id",
    response_model=Reactive_Actuator,
)
def find_reactive_actuator(id: str, request: Request):
    if (
        ra := request.app.database["reactive_actuators"].find_one({"_id": id})
    ) is not None:
        return ra

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Reactive Actuator with ID {id} not found",
    )


@router.put("/{id}", response_description="Update a reactive actuator")
def update_reactive_actuator(id: str, request: Request, ra: RA_Update = Body(...)):
    ra = {k: v for k, v in ra.dict().items() if v is not None}

    if len(ra) >= 1:
        update_result = request.app.database["reactive_actuators"].update_one(
            {"_id": id}, {"$set": ra}
        )

        if update_result.modified_count == 1:
            if (
                updated_ra := request.app.database["reactive_actuators"].find_one(
                    {"_id": id}
                )
            ) is not None:
                return updated_ra

    if (
        existing_reactive_actuator := request.app.database[
            "reactive actuators"
        ].find_one({"_id": id})
    ) is not None:
        return existing_reactive_actuator

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Reactive actuator with ID {id} not found",
    )
