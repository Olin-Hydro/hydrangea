"""
    This code defines Pydantic data models, 'Sensor' and 'SensorUpdate,' for managing sensors and their updates. 
    The models include fields for unique identifiers, names, associated garden identifiers, and timestamps. 
    These models enable structured data validation and documentation support, simplifying the management 
    of sensor data.
"""
import uuid  # Import the 'uuid' module for generating unique identifiers.
import pytz  # Import 'pytz' for timezone support.
from datetime import datetime  # Import 'datetime' for working with timestamps.
from typing import Optional  # Import 'Optional' for type hints.

from pydantic import BaseModel, Field, root_validator  # Import Pydantic components.

# Define a Pydantic data model 'Sensor' for representing sensors.
# TODO: Include list of sensors based on mechanical later
class Sensor(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")  # Unique identifier for the sensor.
    name: str = Field(...)  # Name of the sensor.
    garden_id: str = Field(...)  # Identifier for the associated garden.
    created_at: datetime = datetime.now(pytz.timezone("US/Eastern"))  # Timestamp for sensor creation.
    updated_at: datetime = datetime.now(pytz.timezone("US/Eastern"))  # Timestamp for sensor updates.

    class Config:
        allow_population_by_field_name = True  # Allow populating model fields using dictionary keys.

        # Example data structure for documentation.
        schema_extra = {
            "example": {
                "_id": "5ff70c48-7a56-47fe-b7d9-8df3be3e3197",
                "name": "pH",
                "garden_id": "66608a32-a24c-4b70-ae2c-c46c586ea0c3",
                "created_at": "2023-02-17T20:19:00.541216",
                "updated_at": "2023-02-17T20:19:00.541217",
            }
        }

        @root_validator
        def number_validator(cls, values):
            # Ensure 'updated_at' field is updated when any values change.
            values["updated_at"] = datetime.now(pytz.timezone("US/Eastern"))
            return values

# Define a Pydantic data model 'SensorUpdate' for updating sensor information.
class SensorUpdate(BaseModel):
    name: Optional[str]  # Updated name for the sensor.
    garden_id: Optional[str]  # Updated identifier for the associated garden.
    updated_at: datetime = datetime.now(pytz.timezone("US/Eastern"))  # Timestamp for update.

    class Config:
        schema_extra = {
            "example": {
                "name": "pH",
                "garden_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
            }
        }
