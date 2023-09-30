"""
    This FastAPI code defines an APIRouter for managing gardens and pods within a garden. 
    It provides endpoints to create, list, retrieve, update, and create pods for gardens, 
    with appropriate error handling and database operations.
"""
# Import necessary modules and data models
from typing import List
from fastapi import APIRouter, Body, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from app.models.pod import Pod, PodUpdate
from app.models.garden import Garden, GardenUpdate

# Create an APIRouter instance
router = APIRouter()

# Define the name of the database table for gardens
GARDEN_TABLE_NAME = "gardens"

# Define a route to create a new garden
@router.post(
    "/",
    response_description="Create a new garden",
    status_code=status.HTTP_201_CREATED,
    response_model=Garden,
)
def create_garden(request: Request, garden: Garden = Body(...)):
    # Encode the garden to JSON
    garden = jsonable_encoder(garden)
    
    # Insert the new garden into the database
    new_garden = request.app.database[GARDEN_TABLE_NAME].insert_one(garden)
    
    # Retrieve the created garden from the database
    created_garden = request.app.database[GARDEN_TABLE_NAME].find_one(
        {"_id": new_garden.inserted_id}
    )

    return created_garden

# Define a route to list existing gardens
@router.get(
    "/", response_description="List gardens", response_model=List[Garden]
)
def list_gardens(request: Request, limit: int = 1000):
    # Retrieve and sort gardens by update timestamp
    gardens = list(request.app.database[GARDEN_TABLE_NAME].find())
    gardens.sort(key=lambda r: r["updated_at"], reverse=True)
    
    # Return a limited number of gardens
    return gardens[:limit]

# Define a route to retrieve a single garden by ID
@router.get(
    "/{id}",
    response_description="Get a single garden by id",
    response_model=Garden,
)
def find_garden(id: str, request: Request):
    # Attempt to find the garden by ID in the database
    if (
        garden := request.app.database[GARDEN_TABLE_NAME].find_one({"_id": id})
    ) is not None:
        return garden

    # Raise an exception if the garden is not found
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Garden with ID {id} not found",
    )

# Define a route to list all pods in a garden
@router.get(
    "/{id}/pods",
    response_description="List all pods in the garden",
    response_model=List[Pod],
)
def list_pods(id: str, request: Request):
    # Attempt to find the garden by ID in the database
    if (
        garden := request.app.database[GARDEN_TABLE_NAME].find_one({"_id": id})
    ) is not None:
        return garden["pods"]

    # Raise an exception if the garden is not found
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Garden with ID {id} not found",
    )

# Define a route to update an existing garden
@router.put(
    "/{id}", response_description="Update a garden", response_model=Garden
)
def update_garden(id: str, request: Request, garden: GardenUpdate = Body(...)):
    # Extract non-null fields from the update request
    garden = {k: v for k, v in garden.dict().items() if v is not None}
    
    # Check if there are fields to update
    if len(garden) >= 1:
        # Update the garden in the database
        update_result = request.app.database[GARDEN_TABLE_NAME].update_one(
            {"_id": id}, {"$set": garden}
        )
        
        # Raise an exception if nothing was updated
        if update_result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nothing was updated",
            )
    
    # Retrieve and return the updated or existing garden
    if (
        existing_garden := request.app.database[GARDEN_TABLE_NAME].find_one(
            {"_id": id}
        )
    ) is not None:
        return existing_garden

    # Raise an exception if the garden is not found
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Garden with ID {id} not found",
    )

# Define a route to update an existing pod within a garden
@router.put(
    "/pod/{pod_id}", response_description="Update a pod", response_model=Garden
)
def update_pod(pod_id: str, request: Request, pod: PodUpdate = Body(...)):
    # Define a query to find the garden containing the pod by pod ID
    query = {"pods._id": pod_id}
    
    # Create an update dictionary for the specific pod fields to update
    update = {f"pods.$.{k}": v for k, v in dict(pod).items() if v is not None}
    
    # Attempt to find the garden and update the pod fields
    if (
        pod := request.app.database[GARDEN_TABLE_NAME].find_one(
            query, {"_id": 0, "pods": 1}
        )
    ) is not None:
        # Check if there are fields to update
        if len(update) >= 1:
            # Update the garden in the database
            update_result = request.app.database[GARDEN_TABLE_NAME].update_one(
                query, {"$set": update}
            )
            
            # Raise an exception if nothing was updated
            if update_result.modified_count == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Nothing was updated",
                )
            
            # Return the updated garden
            return request.app.database[GARDEN_TABLE_NAME].find_one(query)
    
    # Raise an exception if the pod is not found
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Pod with ID {pod_id} not found",
    )

# Define a route to create a new pod within a garden
@router.post(
    "/pod/",
    response_description="Create a new pod",
    status_code=status.HTTP_201_CREATED,
)
def create_pod(request: Request, pod: Pod = Body(...)):
    # Encode the pod to JSON
    pod = jsonable_encoder(pod)
    
    # Retrieve the garden ID from the pod data
    garden_id = pod.get("garden_id")
    
    # Define a filter to find the garden by ID
    garden_filter = {"_id": garden_id}

    # Update the garden to add the new pod
    update_result = request.app.database[GARDEN_TABLE_NAME].update_one(
        garden_filter, {"$push": {"pods": pod}}
    )
    
    # Raise an exception if nothing was added
    if update_result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nothing was added",
        )
    
    # Retrieve and return the parent garden with the added pod
    parent_garden = request.app.database[GARDEN_TABLE_NAME].find_one(garden_filter)
    return parent_g
