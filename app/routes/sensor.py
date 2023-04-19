from typing import List

from fastapi import APIRouter, Body, HTTPException, Request, Response, status
from fastapi.encoders import jsonable_encoder

from app.models.sensor import Sensor, SensorUpdate

router = APIRouter()


@router.post(
    "/",
    response_description="Create a new sensor",
    status_code=status.HTTP_201_CREATED,
    response_model=Sensor,
)
def create_sensor(request: Request, sensor: Sensor = Body(...)):
    sensor = jsonable_encoder(sensor)
    garden_id = sensor.get("garden_id")
    if (
        request.app.database["gardens"].find_one({"_id": garden_id})
    ) is not None:
        new_sensor = request.app.database["sensors"].insert_one(sensor)
        created_sensor = request.app.database["sensors"].find_one(
            {"_id": new_sensor.inserted_id}
        )
        return created_sensor
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Sensor with garden ID {garden_id} not found",
    )


@router.get(
    "/", response_description="List sensors", response_model=List[Sensor]
)
def list_sensors(request: Request, limit: int = 1000):
    sensors = list(request.app.database["sensors"].find())
    sensors.sort(key=lambda r: r["updated_at"], reverse=True)
    return sensors[:limit]


@router.get(
    "/{id}",
    response_description="Get a single sensor by id",
    response_model=Sensor,
)
def find_sensor(id: str, request: Request):
    if (
        sensor := request.app.database["sensors"].find_one({"_id": id})
    ) is not None:
        return sensor

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Sensor with ID {id} not found",
    )


@router.put(
    "/{id}", response_description="Update a sensor", response_model=Sensor
)
def update_sensor(id: str, request: Request, sensor: SensorUpdate = Body(...)):
    sensor = {k: v for k, v in sensor.dict().items() if v is not None}

    if len(sensor) >= 1:
        update_result = request.app.database["sensors"].update_one(
            {"_id": id}, {"$set": sensor}
        )

        if update_result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sensor with ID {id} not found",
            )

    if (
        existing_sensor := request.app.database["sensors"].find_one(
            {"_id": id}
        )
    ) is not None:
        return existing_sensor

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Sensor with ID {id} not found",
    )


@router.delete("/{id}", response_description="Delete a sensor")
def delete_sensor(id: str, request: Request, response: Response):
    delete_result = request.app.database["sensors"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Sensor with ID {id} not found",
    )
