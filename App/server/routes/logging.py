import sys
from typing import List


from fastapi import APIRouter, Body, HTTPException, Request, status, Query
from fastapi.encoders import jsonable_encoder

try:
    from App.server.models.logging import Reading, Scheduled_Action, Reactive_Action
except ModuleNotFoundError:
    sys.path.append("../server")
    from server.models.logging import Reading, Scheduled_Action, Reactive_Action

router = APIRouter()


@router.post(
    "/sensors/logging/",
    response_description="Create a new sensor reading",
    status_code=status.HTTP_201_CREATED,
    response_model=Reading,
)
def create_reactive_actuator(request: Request, reading: Reading = Body(...)):
    reading = jsonable_encoder(reading)
    sensor_id = reading.get("sensor_id")
    if (request.app.database["sensors"].find_one({"_id": sensor_id})) is not None:
        new_reading = request.app.database["readings"].insert_one(reading)
        created_reading = request.app.database["readings"].find_one(
            {"_id": new_reading.inserted_id}
        )
        return created_reading
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Reading with Sensor ID {sensor_id} not found",
    )


@router.get(
    "/sensors/logging/",
    response_description="List readings for all sensor in the given time period",
    response_model=List[Reading],
)
def list_readings(
    request: Request,
    limit: int = 1000,
    start: str = Query(default=...),
    end: str = Query(default=...),
):
    if (
        len(
            readings := list(
                request.app.database["readings"].find(
                    {"created_at": {"$gte": start, "$lt": end}}
                )
            )
        )
        is not 0
    ):
        readings.sort(key=lambda r: r["updated_at"], reverse=True)
        return readings[:limit]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No actions were found within the time period",
    )


@router.get(
    "/sensors/logging/{sensor_id}",
    response_description="List readings for a specific sensor in the given time period",
    response_model=List[Reading],
)
def find_readings(
    sensor_id,
    request: Request,
    limit: int = 1000,
    start: str = Query(default=...),
    end: str = Query(default=...),
):
    if (
        len(
            readings := list(
                request.app.database["readings"].find(
                    {"sensor_id": sensor_id, "created_at": {"$gte": start, "$lt": end}}
                )
            )
        )
        is not 0
    ):
        readings.sort(key=lambda r: r["updated_at"], reverse=True)
        return readings[:limit]

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Reading for sensor with ID {sensor_id} not found or no readings were found within the time period",
    )


@router.post(
    "/sa/logging/actions/",
    response_description="Create a new scheduled action",
    status_code=status.HTTP_201_CREATED,
    response_model=Scheduled_Action,
)
def create_scheduled_action(request: Request, scheduled_action: Reading = Body(...)):
    scheduled_action = jsonable_encoder(scheduled_action)
    actuator_id = scheduled_action.get("actuator_id")
    if (
        len(request.app.database["scheduled_actuators"].find_one({"_id": actuator_id}))
        is not 0
    ):
        new_scheduled_action = request.app.database["scheduled_actions"].insert_one(
            scheduled_action
        )
        created_scheduled_action = request.app.database["scheduled_actions"].find_one(
            {"_id": new_scheduled_action.inserted_id}
        )
        return created_scheduled_action
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Scheduled action for actuator with ID {actuator_id} not found",
    )


@router.get(
    "/sa/logging/actions/",
    response_description="List all scheduled actions in the given time period",
    response_model=List[Scheduled_Action],
)
def list_scheduled_actions(
    request: Request,
    limit: int = 1000,
    start: str = Query(default=...),
    end: str = Query(default=...),
):
    if (
        len(
            scheduled_actions := list(
                request.app.database["scheduled_actions"].find(
                    {"created_at": {"$gte": start, "$lt": end}}
                )
            )
        )
        is not 0
    ):
        scheduled_actions.sort(key=lambda r: r["updated_at"], reverse=True)
        return scheduled_actions[:limit]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No actions were found within the time period",
    )


@router.get(
    "/sa/logging/actions/{id}",
    response_description="List scheduled actions for a specific actuator in the given time period",
    response_model=List[Scheduled_Action],
)
def find_scheduled_actions(
    actuator_id,
    request: Request,
    limit: int = 1000,
    start: str = Query(default=...),
    end: str = Query(default=...),
):
    if (
        len(
            scheduled_actions := list(
                request.app.database["scheduled_actions"].find(
                    {
                        "actuator_id": actuator_id,
                        "created_at": {"$gte": start, "$lt": end},
                    }
                )
            )
        )
        is not 0
    ):
        scheduled_actions.sort(key=lambda r: r["updated_at"], reverse=True)
        return scheduled_actions[:limit]

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Scheduled action for actuator with ID {actuator_id} not found or no actions were found within the time period",
    )


@router.post(
    "/ra/logging/actions/",
    response_description="Create a new reactive action",
    status_code=status.HTTP_201_CREATED,
    response_model=Reactive_Action,
)
def create_reactive_action(
    request: Request, reactive_action: Reactive_Action = Body(...)
):
    reactive_action = jsonable_encoder(reactive_action)
    actuator_id = reactive_action.get("actuator_id")
    if (
        len(request.app.database["reactive_actuators"].find_one({"_id": actuator_id}))
        is not 0
    ):
        new_reactive_action = request.app.database["reactive_actions"].insert_one(
            reactive_action
        )
        created_reactive_action = request.app.database["reactive_actions"].find_one(
            {"_id": new_reactive_action.inserted_id}
        )
        return created_reactive_action
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Reactive action for actuator with ID {actuator_id} not found",
    )


@router.get(
    "/ra/logging/actions/",
    response_description="List all reactive actions in the given time period",
    response_model=List[Reactive_Action],
)
def list_reactive_actions(
    request: Request,
    limit: int = 1000,
    start: str = Query(default=...),
    end: str = Query(default=...),
):
    if (
        len(
            reactive_actions := list(
                request.app.database["reactive_actions"].find(
                    {"created_at": {"$gte": start, "$lt": end}}
                )
            )
        )
        is not 0
    ):
        reactive_actions.sort(key=lambda r: r["updated_at"], reverse=True)
        return reactive_actions[:limit]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No actions were found within the time period",
    )


@router.get(
    "/ra/logging/actions/{id}",
    response_description="List reactive actions for a specific actuator in the given time period",
    response_model=List[Reactive_Action],
)
def find_reactive_actions(
    actuator_id,
    request: Request,
    limit: int = 1000,
    start: str = Query(default=...),
    end: str = Query(default=...),
):
    if (
        len(
            reactive_actions := list(
                request.app.database["reactive_actions"].find(
                    {
                        "actuator_id": actuator_id,
                        "created_at": {"$gte": start, "$lt": end},
                    }
                )
            )
        )
        is not 0
    ):
        reactive_actions.sort(key=lambda r: r["updated_at"], reverse=True)
        return reactive_actions[:limit]

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Reactive action for actuator with ID {actuator_id} not found or no actions were found within the time period",
    )
