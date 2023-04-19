from typing import List

from fastapi import APIRouter, Body, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder

from app.models.pod import Pod, PodUpdate
from app.models.garden import Garden, GardenUpdate


router = APIRouter()


@router.post(
    "/",
    response_description="Create a new garden",
    status_code=status.HTTP_201_CREATED,
    response_model=Garden,
)
def create_garden(request: Request, garden: Garden = Body(...)):
    garden = jsonable_encoder(garden)
    new_garden = request.app.database["gardens"].insert_one(garden)
    created_garden = request.app.database["gardens"].find_one(
        {"_id": new_garden.inserted_id}
    )

    return created_garden


@router.get(
    "/", response_description="List gardens", response_model=List[Garden]
)
def list_gardens(request: Request, limit: int = 1000):
    gardens = list(request.app.database["gardens"].find())
    gardens.sort(key=lambda r: r["updated_at"], reverse=True)
    return gardens[:limit]


@router.get(
    "/{id}",
    response_description="Get a single garden by id",
    response_model=Garden,
)
def find_garden(id: str, request: Request):
    if (
        garden := request.app.database["gardens"].find_one({"_id": id})
    ) is not None:
        return garden

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Garden with ID {id} not found",
    )


@router.get(
    "/{id}/pods",
    response_description="List all pods in the garden",
    response_model=List[Pod],
)
def list_pods(id: str, request: Request):
    if (
        garden := request.app.database["gardens"].find_one({"_id": id})
    ) is not None:
        return garden["pods"]

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Garden with ID {id} not found",
    )


@router.put(
    "/{id}", response_description="Update a garden", response_model=Garden
)
def update_garden(id: str, request: Request, garden: GardenUpdate = Body(...)):
    garden = {k: v for k, v in garden.dict().items() if v is not None}
    if len(garden) >= 1:
        update_result = request.app.database["gardens"].update_one(
            {"_id": id}, {"$set": garden}
        )
        if update_result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nothing was updated",
            )

    if (
        existing_garden := request.app.database["gardens"].find_one(
            {"_id": id}
        )
    ) is not None:
        return existing_garden

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Garden with ID {id} not found",
    )


@router.put(
    "/pod/{pod_id}", response_description="Update a pod", response_model=Garden
)
def update_pod(pod_id: str, request: Request, pod: PodUpdate = Body(...)):
    query = {"pods._id": pod_id}
    update = {f"pods.$.{k}": v for k, v in dict(pod).items() if v is not None}
    if (
        pod := request.app.database["gardens"].find_one(
            query, {"_id": 0, "pods": 1}
        )
    ) is not None:
        if len(update) >= 1:
            update_result = request.app.database["gardens"].update_one(
                query, {"$set": update}
            )
            if update_result.modified_count == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Nothing was updated",
                )
            return request.app.database["gardens"].find_one(query)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Pod with ID {pod_id} not found",
    )


@router.post(
    "/pod/",
    response_description="Create a new pod",
    status_code=status.HTTP_201_CREATED,
)
def create_pod(request: Request, pod: Pod = Body(...)):
    pod = jsonable_encoder(pod)
    garden_id = pod.get("garden_id")
    garden_filter = {"_id": garden_id}

    update_result = request.app.database["gardens"].update_one(
        garden_filter, {"$push": {"pods": pod}}
    )
    if update_result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nothing was added",
        )
    parent_garden = request.app.database["gardens"].find_one(garden_filter)
    return parent_garden
