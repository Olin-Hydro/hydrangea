"""
    The code defines Pydantic data models for managing schedules and configurations related to sensors, 
    Smart Actuators (SA), and Reactive Actuators (RA). It includes fields for unique identifiers, scheduling 
    parameters, and timestamps, offering structured data validation and documentation support.
"""
import uuid  # Import the 'uuid' module for generating unique identifiers.
from datetime import datetime  # Import 'datetime' for working with timestamps.
from typing import Optional, List  # Import 'Optional' and 'List' for type hints.
import pytz  # Import 'pytz' for timezone support.

from pydantic import BaseModel, Field, root_validator  # Import Pydantic components.

# Define a Pydantic data model 'SASchedule' for scheduling Smart Actuators (SA).
class SASchedule(BaseModel):
    sa_id: str = Field(...)  # Identifier for the Smart Actuator.
    on: List[datetime] = Field(...)  # List of scheduled activation times.
    off: List[datetime] = Field(...)  # List of scheduled deactivation times.

# Define a Pydantic data model 'SensorSchedule' for scheduling sensors.
class SensorSchedule(BaseModel):
    sensor_id: str = Field(...)  # Identifier for the sensor.
    interval: float = Field(...)  # Measurement interval for the sensor.

# Define a Pydantic data model 'RASchedule' for scheduling Reactive Actuators (RA).
class RASchedule(BaseModel):
    ra_id: str = Field(...)  # Identifier for the Reactive Actuator.
    interval: float = Field(...)  # Interval for performing reactive actions.
    threshold: float = Field(...)  # Threshold value for activation.
    duration: float = Field(...)  # Duration of the reactive action.
    threshold_type: int = Field(...)  # Type of threshold (1: ceiling, 0: floor).

# Define a Pydantic data model 'Config' for representing configuration settings.
class Config(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")  # Unique identifier for the configuration.
    name: str = Field(...)  # Name of the configuration.
    sensor_schedule: List[SensorSchedule] = Field(...)  # List of sensor schedules.
    ra_schedule: List[RASchedule] = Field(...)  # List of Reactive Actuator schedules.
    sa_schedule: List[SASchedule] = Field(...)  # List of Smart Actuator schedules.
    created_at: datetime = datetime.now(pytz.timezone("US/Eastern"))  # Timestamp for configuration creation.
    updated_at: datetime = datetime.now(pytz.timezone("US/Eastern"))  # Timestamp for configuration updates.

    class Config:
        allow_population_by_field_name = True  # Allow populating model fields using dictionary keys.

        # Example data structure for documentation.
        schema_extra = {
            "example": {
                "_id": "b67cd1cf-e113-40cf-a293-ba80251e03ce",
                "name": "TestConfig",
                "sensor_schedule": [
                    {
                        "sensor_id": "66608a32-a24c-4b70-ae2c-c46c586ea0c3",
                        "interval": 300.0,
                    }
                ],
                "ra_schedule": [
                    {
                        "ra_id": "5e9b44c7-970a-41f0-8ef4-e4dbf82f00c3",
                        "interval": 1200.0,
                        "threshold": 7.5,
                        "duration": 5.0,
                        "threshold_type": 1,
                    }
                ],
                "sa_schedule": [
                    {
                        "sa_id": "15a2a241-cf21-4365-af45-3d140712f2b8",
                        "on": [
                            "2023-02-17T08:09:50+00:00",
                            "2023-02-17T16:09:50+00:00",
                            "2023-02-17T20:09:50+00:00",
                        ],
                        "off": [
                            "2023-02-17T08:29:50+00:00",
                            "2023-02-17T16:29:50+00:00",
                            "2023-02-17T20:29:50+00:00",
                        ],
                    }
                ],
                "created_at": "2023-02-18T21:15:12.005399",
                "updated_at": "2023-02-18T21:15:12.005400",
            }
        }

        @root_validator
        def number_validator(cls, values):
            # Ensure 'updated_at' field is updated when any values change.
            values["updated_at"] = datetime.now(pytz.timezone("US/Eastern"))
            return values

# Define a Pydantic data model 'ConfigUpdate' for updating configuration settings.
class ConfigUpdate(BaseModel):
    name: Optional[str]  # Updated name for the configuration.
    sensor_schedule: Optional[List[SensorSchedule]]  # Updated sensor schedules.
    ra_schedule: Optional[List[RASchedule]]  # Updated Reactive Actuator schedules.
    sa_schedule: Optional[List[SASchedule]]  # Updated Smart Actuator schedules.
    updated_at: datetime = datetime.now(pytz.timezone("US/Eastern"))  # Timestamp for update.

    class Config:
        # Example data structure for documentation.
        schema_extra = {
            "example": {
                "name": "Config 1",
                "sensor_schedule": [{"sensor_id": "abc", "interval": 400}],
            }
        }
