"""
    This code defines Pydantic data models, 'Reactive_Actuator' and 'RA_Update,' for managing reactive 
    actuators and their updates. The models include fields for unique identifiers, names, associated 
    sensor identifiers, and timestamps. These models enable structured data validation and documentation 
    support, simplifying the management of reactive actuator data.
"""

import uuid  # Import the 'uuid' module for generating unique identifiers.
import pytz  # Import 'pytz' for timezone support.
from datetime import datetime  # Import 'datetime' for working with timestamps.
from typing import Optional  # Import 'Optional' for type hints.

from pydantic import BaseModel, Field, root_validator  # Import Pydantic components.

# Define a Pydantic data model 'Reactive_Actuator' for representing reactive actuators.
# TODO: Add examples/list of reactive actuators based on mechanical later?
class Reactive_Actuator(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")  # Unique identifier for the reactive actuator.
    name: str = Field(...)  # Name of the reactive actuator.
    sensor_id: str = Field(...)  # Identifier for the associated sensor.
    created_at: datetime = datetime.now(pytz.timezone("US/Eastern"))  # Timestamp for actuator creation.
    updated_at: datetime = datetime.now(pytz.timezone("US/Eastern"))  # Timestamp for actuator updates.

    class Config:
        allow_population_by_field_name = True  # Allow populating model fields using dictionary keys.

        # Example data structure for documentation.
        schema_extra = {
            "example": {
                "_id": "5e9b44c7-970a-41f0-8ef4-e4dbf82f00c3",
                "name": "ph down pump",
                "sensor_id": "5ff70c48-7a56-47fe-b7d9-8df3be3e3197",
                "created_at": "2023-02-17T20:19:00.549263",
                "updated_at": "2023-02-17T20:19:00.549264",
            }
        }

        @root_validator
        def number_validator(cls, values):
            # Ensure 'updated_at' field is updated when any values change.
            values["updated_at"] = datetime.now(pytz.timezone("US/Eastern"))
            return values

# Define a Pydantic data model 'RA_Update' for updating reactive actuator information.
class RA_Update(BaseModel):
    name: Optional[str]  # Updated name for the reactive actuator.
    sensor_id: Optional[str]  # Updated identifier for the associated sensor.
    updated_at: datetime = datetime.now(pytz.timezone("US/Eastern"))  # Timestamp for update.

    class Config:
        schema_extra = {
            "example": {"name": "Don Quixote", "sensor_id": "a47a4b121"}
        }
