"""
    This code defines Pydantic data models, 'Pod' and 'PodUpdate,' for managing garden pods and 
    their updates, including fields for unique identifiers, names, locations, associated gardens, 
    and plant types. These models facilitate structured data validation and documentation support, 
    contributing to the efficient management of garden pod data.
"""

import uuid  # Import the 'uuid' module for generating unique identifiers.
from datetime import datetime  # Import 'datetime' for working with timestamps.
from typing import Optional, List  # Import 'Optional' and 'List' for type hints.
import pytz  # Import 'pytz' for timezone support.

from pydantic import BaseModel, Field, root_validator  # Import Pydantic components.

# Define a Pydantic data model 'Pod' for representing garden pods.
class Pod(BaseModel):
    pod_id: Optional[str] = Field(default_factory=uuid.uuid4, alias="_id")  # Unique identifier for the pod (optional).
    name: str = Field(...)  # Name of the pod.
    garden_id: str = Field(...)  # Identifier for the associated garden.
    location: List[int] = Field(...)  # Location of the pod, represented as [row, column].
    plant: str = None  # Type of plant in the pod (optional).
    created_at: datetime = datetime.now(pytz.timezone("US/Eastern"))  # Timestamp for pod creation.
    updated_at: datetime = datetime.now(pytz.timezone("US/Eastern"))  # Timestamp for pod updates.

    class Config:
        allow_population_by_field_name = True  # Allow populating model fields using dictionary keys.

        # Example data structure for documentation.
        schema_extra = {
            "example": {
                "_id": "66608a32-a24c-4b70-ae2c-c46c586ea0c3",
                "name": "John Geddes Basil",
                "garden_id": "77608a32-a45c-4b70-ae2c-c46c586ea0c3",
                "location": [1, 3],
                "plant": "Basil",
                "created_at": "2023-02-17T20:19:00.536083",
                "updated_at": "2023-02-17T20:19:00.536084",
            }
        }

        @root_validator
        def number_validator(cls, values):
            # Ensure 'updated_at' field is updated when any values change.
            values["updated_at"] = datetime.now(pytz.timezone("US/Eastern"))
            return values

# Define a Pydantic data model 'PodUpdate' for updating pod information.
class PodUpdate(BaseModel):
    name: Optional[str]  # Updated name for the pod.
    garden_id: Optional[str]  # Updated identifier for the associated garden.
    location: Optional[List[int]]  # Updated location of the pod, represented as [row, column].
    plant: Optional[str]  # Updated type of plant in the pod (optional).
    updated_at: datetime = datetime.now(pytz.timezone("US/Eastern"))  # Timestamp for update.

    class Config:
        schema_extra = {
            "example": {
                "name": "Jack Lettuce",
                "garden_id": "77608a32-a45c-4b70-ae2c-c46c586ea0c3",
                "location": [2, 6],
                "plant": "Lettuce",
            }
        }
