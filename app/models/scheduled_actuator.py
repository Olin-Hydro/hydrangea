"""
    This code defines Pydantic data models, 'Scheduled_Actuator' and 'SA_Update,' for 
    managing scheduled actuators and their updates. The models include fields for unique 
    identifiers, names, associated garden identifiers, and timestamps. These models enable 
    structured data validation and documentation support, simplifying the management of 
    scheduled actuator data.
"""

import uuid  # Import the 'uuid' module for generating unique identifiers.
import pytz  # Import 'pytz' for timezone support.
from datetime import datetime  # Import 'datetime' for working with timestamps.
from typing import Optional  # Import 'Optional' for type hints.

from pydantic import BaseModel, Field, root_validator  # Import Pydantic components.

# Define a Pydantic data model 'Scheduled_Actuator' for representing scheduled actuators.
# TODO: Add list of scheduled actuators based on mechanical later.
class Scheduled_Actuator(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")  # Unique identifier for the scheduled actuator.
    name: str = Field(...)  # Name of the scheduled actuator.
    garden_id: str = Field(...)  # Identifier for the associated garden.
    created_at: datetime = datetime.now(pytz.timezone("US/Eastern"))  # Timestamp for actuator creation.
    updated_at: datetime = datetime.now(pytz.timezone("US/Eastern"))  # Timestamp for actuator updates.

    class Config:
        allow_population_by_field_name = True  # Allow populating model fields using dictionary keys.

        # Example data structure for documentation.
        schema_extra = {
            "example": {
                "_id": "15a2a241-cf21-4365-af45-3d140712f2b8",
                "name": "water pump",
                "garden_id": "66608a32-a24c-4b70-ae2c-c46c586ea0c3",
                "created_at": "2023-02-17T20:19:00.545693",
                "updated_at": "2023-02-17T20:19:00.545694",
            }
        }

        @root_validator
        def number_validator(cls, values):
            # Ensure 'updated_at' field is updated when any values change.
            values["updated_at"] = datetime.now(pytz.timezone("US/Eastern"))
            return values

# Define a Pydantic data model 'SA_Update' for updating scheduled actuator information.
class SA_Update(BaseModel):
    name: Optional[str]  # Updated name for the scheduled actuator.
    garden_id: Optional[str]  # Updated identifier for the associated garden.
    updated_at: datetime = datetime.now(pytz.timezone("US/Eastern"))  # Timestamp for update.

    class Config:
        schema_extra = {
            "example": {"name": "Don Quixote", "garden_id": "a47a4b121"}
        }
