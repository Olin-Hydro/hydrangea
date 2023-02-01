import sys
from typing import List


from fastapi import APIRouter, Body, HTTPException, Request, status

# delete import of Response ^^^
from fastapi.encoders import jsonable_encoder

try:
    from App.server.models.scheduled_actuator import Scheduled_Actuator, SA_Update
except ModuleNotFoundError:
    sys.path.append("../server")
    from server.models.scheduled_actuator import Scheduled_Actuator, SA_Update

router = APIRouter()


@router.post(
    "/",
    response_description="Create a new scheduled actuator",
    status_code=status.HTTP_201_CREATED,
    response_model=Scheduled_Actuator,
)
def create_scheduled_actuator(
    request: Request, scheduled_actuator: Scheduled_Actuator = Body(...)
):
    sa = jsonable_encoder(scheduled_actuator)
    new_sa = request.app.database["scheduled actuator"].insert_one(sa)
    created_sa = request.app.database["scheduled actuators"].find_one(
        {"_id": new_sa.inserted_id}
    )

    return created_sa


@router.get(
    "/",
    response_description="List scheduled actuators",
    response_model=List[Scheduled_Actuator],
)
def list_scheduled_actuators(request: Request, limit: int = 1000):
    scheduled_actuators = list(request.app.database["scheduled actuators"].find())
    scheduled_actuators.sort(key=lambda r: r["updated_at"], reverse=True)

    return scheduled_actuators[:limit]


@router.get(
    "/{id}",
    response_description="Get a single scheduled actuator by id",
    response_model=Scheduled_Actuator,
)
def find_scheduled_actuator(id: str, request: Request):
    if (
        sa := request.app.database["scheduled_actuator"].find_one({"_id": id})
    ) is not None:
        return sa

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Scheduled Actuator with ID {id} not found",
    )


# http put operation - https://fastapi.tiangolo.com/tutorial/body-updates/?h=put#update-replacing-with-put


@router.put("/{id}", response_description="Update a scheduled actuator")
def update_scheduled_actuator(id: str, request: Request, sa: SA_Update = Body(...)):
    sa = {k: v for k, v in sa.dict().items() if v is not None}

    if len(sa) >= 1:
        update_result = request.app.database["scheduled actuators"].update_one(
            {"_id": id}, {"$set": sa}
        )

        if update_result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Scheduled Actuator with ID {id} not found",
            )
    if (
        existing_scheduled_actuator := request.app.database[
            "scheduled actuators"
        ].find_one({"_id": id})
    ) is not None:
        return existing_scheduled_actuator

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Scheduled actuator with ID {id} not found",
    )
