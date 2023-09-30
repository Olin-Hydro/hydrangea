"""
    This FastAPI code defines API routes for creating, listing, retrieving, and updating 
    configuration settings in a web application. It uses data models for structured input
    and output, allowing users to interact with configuration data stored in a database.
"""

# Import necessary modules and classes
from typing import List
from fastapi import APIRouter, Body, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder

# Import data models for configuration and configuration updates
from app.models.config import Config, ConfigUpdate

# Create an APIRouter instance
router = APIRouter()

# Define the name of the database table for configurations
CONFIG_TABLE_NAME = "configs"

# Define a route to create a new configuration
@router.post(
    "/",
    response_description="Create a new config",
    status_code=status.HTTP_201_CREATED,
    response_model=Config,
)
def create_config(request: Request, config: Config = Body(...)):
    # Encode the configuration to JSON
    conf = jsonable_encoder(config)
    
    # Insert the new configuration into the database
    new_config = request.app.database[CONFIG_TABLE_NAME].insert_one(conf)
    
    # Retrieve the created configuration from the database
    created_config = request.app.database[CONFIG_TABLE_NAME].find_one(
        {"_id": new_config.inserted_id}
    )

    return created_config

# Define a route to list existing configurations
@router.get(
    "/", response_description="List configs", response_model=List[Config]
)
def list_configs(request: Request, limit: int = 1000):
    # Retrieve and sort configurations by update timestamp
    configs = list(request.app.database[CONFIG_TABLE_NAME].find())
    configs.sort(key=lambda r: r["updated_at"], reverse=True)
    
    # Return a limited number of configurations
    return configs[:limit]

# Define a route to retrieve a single configuration by ID
@router.get(
    "/{id}",
    response_description="Get a single config by id",
    response_model=Config,
)
def find_config(id: str, request: Request):
    # Attempt to find the configuration by ID in the database
    if (
        config := request.app.database[CONFIG_TABLE_NAME].find_one({"_id": id})
    ) is not None:
        return config

    # Raise an exception if the configuration is not found
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Config with ID {id} not found",
    )

# Define a route to update an existing configuration
@router.put(
    "/{id}", response_description="Update a config", response_model=Config
)
def update_config(id: str, request: Request, config: ConfigUpdate = Body(...)):
    # Extract non-null fields from the update request
    config = {k: v for k, v in config.dict().items() if v is not None}
    
    # Check if there are fields to update
    if len(config) >= 1:
        # Update the configuration in the database
        update_result = request.app.database[CONFIG_TABLE_NAME].update_one(
            {"_id": id}, {"$set": config}
        )
        
        # Raise an exception if the configuration is not found
        if update_result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Config with ID {id} not found",
            )
    
    # Retrieve and return the updated or existing configuration
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
