"""
    This code defines Pydantic data models for representing sensor readings, scheduled actions, and reactive actions, 
    including fields for unique identifiers, associated data, and timestamps. These models enable structured data 
    validation and documentation support, aiding in the management of sensor data and actuator actions.
"""

import uuid  # Import the 'uuid' module for generating unique identifiers.
import pytz  # Import 'pytz' for timezone support.
from datetime import datetime  # Import 'datetime' for working with timestamps.
from pydantic import BaseModel, Field, root_validator  # Import Pydantic components.

# Define a Pydantic data model 'Reading' for representing sensor readings.
class Reading(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")  # Unique identifier for the reading.
    sensor_id: str = Field(...)  # Identifier for the sensor.
    value: float = Field(...)  # Value of the sensor reading.
    created_at: datetime = datetime.now(pytz.timezone("US/Eastern"))  # Timestamp for reading creation.
    updated_at: datetime = datetime.now(pytz.timezone("US/Eastern"))  # Timestamp for reading updates.

    class Config:
        allow_population_by_field_name = True  # Allow populating model fields using dictionary keys.

        # Example data structure for documentation.
        schema_extra = {
            "example": {
                "sensor_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "value": "5",
            }
        }

        @root_validator
        def number_validator(cls, values):
            # Ensure 'updated_at' field is updated when any values change.
            values["updated_at"] = datetime.now(pytz.timezone("US/Eastern"))
            return values

# Define a Pydantic data model 'Scheduled_Action' for representing scheduled actions.
class Scheduled_Action(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")  # Unique identifier for the scheduled action.
    actuator_id: str = Field(...)  # Identifier for the actuator.
    data: str = Field(...)  # Data associated with the scheduled action.
    created_at: datetime = datetime.now(pytz.timezone("US/Eastern"))  # Timestamp for action creation.
    updated_at: datetime = datetime.now(pytz.timezone("US/Eastern"))  # Timestamp for action updates.

    class Config:
        allow_population_by_field_name = True  # Allow populating model fields using dictionary keys.

        # Example data structure for documentation.
        schema_extra = {
            "example": {
                "actuator_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "data": "5",
            }
        }

        @root_validator
        def number_validator(cls, values):
            # Ensure 'updated_at' field is updated when any values change.
            values["updated_at"] = datetime.now(pytz.timezone("US/Eastern"))
            return values

# Define a Pydantic data model 'Reactive_Action' for representing reactive actions.
class Reactive_Action(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")  # Unique identifier for the reactive action.
    actuator_id: str = Field(...)  # Identifier for the actuator.
    data: str = Field(...)  # Data associated with the reactive action.
    created_at: datetime = datetime.now(pytz.timezone("US/Eastern"))  # Timestamp for action creation.
    updated_at: datetime = datetime.now(pytz.timezone("US/Eastern"))  # Timestamp for action updates.

    class Config:
        allow_population_by_field_name = True  # Allow populating model fields using dictionary keys.

        # Example data structure for documentation.
        schema_extra = {
            "example": {
                "actuator_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "data": "on",
            }
        }

        @root_validator
        def number_validator(cls, values):
            # Ensure 'updated_at' field is updated when any values change.
            values["updated_at"] = datetime.now(pytz.timezone("US/Eastern"))
            return values
