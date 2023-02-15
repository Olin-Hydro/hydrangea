import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, root_validator


class Reading(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    sensor_id: str = Field(...)
    value: float = Field(...)
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "sensor_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "value": "5",
            }
        }

        @root_validator
        def number_validator(cls, values):
            values["updated_at"] = datetime.utcnow()
            return values


class Scheduled_Action(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    actuator_id: str = Field(...)
    data: str = Field(...)
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "actuator_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "data": "5",
            }
        }

        @root_validator
        def number_validator(cls, values):
            values["updated_at"] = datetime.utcnow()
            return values


class Reactive_Action(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    actuator_id: str = Field(...)
    data: str = Field(...)
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "actuator_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "data": "on",
            }
        }

        @root_validator
        def number_validator(cls, values):
            values["updated_at"] = datetime.utcnow()
            return values
