"""
    The  code defines Pydantic data models, 'Garden' and 'GardenUpdate,' for managing garden information
    and updates, including fields for identifiers, names, locations, associated configurations, 
    and pods. These models enable structured data validation and offer example data structures 
    for documentation, contributing to the efficient management of garden-related data.
"""
import uuid  # Import the 'uuid' module for generating unique identifiers.
from datetime import datetime  # Import 'datetime' for working with timestamps.
from typing import Optional, Union, List  # Import 'Optional', 'Union', and 'List' for type hints.
import pytz  # Import 'pytz' for timezone support.

from pydantic import BaseModel, Field, root_validator  # Import Pydantic components.
from app.models.pod import Pod, PodUpdate  # Import related models.

# Define a Pydantic data model 'Garden' for representing garden information.
class Garden(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")  # Unique identifier for the garden.
    name: str = Field(...)  # Name of the garden.
    location: str = Field(...)  # Location of the garden.
    config_id: Optional[str] = None  # Identifier of the associated configuration (optional).
    pods: Optional[List[Pod]] = None  # List of pods associated with the garden (optional).
    created_at: datetime = datetime.now(pytz.timezone("US/Eastern"))  # Timestamp for garden creation.
    updated_at: datetime = datetime.now(pytz.timezone("US/Eastern"))  # Timestamp for garden updates.

    class Config:
        allow_population_by_field_name = True  # Allow populating model fields using dictionary keys.

        # Example data structure for documentation.
        schema_extra = {
            "example": {
                "_id": "66608a32-a24c-4b70-ae2c-c46c586ea0c3",
                "name": "Og Garden",
                "location": "3rd Floor Endcap",
                "config_id": "77608a32-a45c-4b70-ae2c-c46c586ea0c3",
                "pods": [
                    {
                        "_id": "66608a32-a24c-4b70-ae2c-c46c586ea0c3",
                        "name": "Johns Lettuce",
                        "garden_id": "77608a32-a45c-4b70-ae2c-c46c586ea0c3",
                        "location": [1, 3],
                        "plant": "Lettuce",
                        "created_at": "2023-02-17T20:19:00.536083",
                        "updated_at": "2023-02-17T20:19:00.536084",
                    }
                ],
                "created_at": "2023-02-17T20:19:00.536083",
                "updated_at": "2023-02-17T20:19:00.536084",
            }
        }

        @root_validator
        def number_validator(cls, values):
            # Ensure 'updated_at' field is updated when any values change.
            values["updated_at"] = datetime.now(pytz.timezone("US/Eastern"))
            return values

# Define a Pydantic data model 'GardenUpdate' for updating garden information.
class GardenUpdate(BaseModel):
    name: Optional[str]  # Updated name for the garden.
    location: Optional[str]  # Updated location for the garden.
    config_id: Optional[str]  # Updated configuration identifier.
    pods: Union[List[Pod], List[PodUpdate], None]  # Updated list of pods or pod updates (optional).
    updated_at: datetime = datetime.now(pytz.timezone("US/Eastern"))  # Timestamp for update.

    class Config:
        # Example data structure for documentation.
        schema_extra = {
            "example": {
                "name": "Don Quixote",
                "location": "Miguel de Cervantes",
                "config_id": "abcd",
                "pods": [
                    {
                        "_id": "66608a32-a24c-4b70-ae2c-c46c586ea0c3",
                        "name": "Johns Lettuce",
                        "garden_id": "77608a32-a45c-4b70-ae2c-c46c586ea0c3",
                        "location": [1, 3],
                        "plant": "Lettuce",
                        "created_at": "2023-02-17T20:19:00.536083",
                        "updated_at": "2023-02-17T20:19:00.536084",
                    }
                ],
            }
        }
