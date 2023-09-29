import uuid
import pytz
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class Reading(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    sensor_id: str = Field(...)
    value: float = Field(...)
    created_at: datetime = datetime.now(pytz.timezone("US/Eastern"))
    updated_at: datetime = datetime.now(pytz.timezone("US/Eastern"))

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "sensor_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "value": "5",
            }
        }

        @field_validator("updated_at")
        def number_validator(cls, values):
            values["updated_at"] = datetime.now(pytz.timezone("US/Eastern"))
            return values


class Scheduled_Action(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    actuator_id: str = Field(...)
    data: str = Field(...)
    created_at: datetime = datetime.now(pytz.timezone("US/Eastern"))
    updated_at: datetime = datetime.now(pytz.timezone("US/Eastern"))

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "actuator_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "data": "5",
            }
        }

        @field_validator("updated_at")
        def number_validator(cls, values):
            values["updated_at"] = datetime.now(pytz.timezone("US/Eastern"))
            return values


class Reactive_Action(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    actuator_id: str = Field(...)
    data: str = Field(...)
    created_at: datetime = datetime.now(pytz.timezone("US/Eastern"))
    updated_at: datetime = datetime.now(pytz.timezone("US/Eastern"))

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "actuator_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "data": "on",
            }
        }

        @field_validator("updated_at")
        def number_validator(cls, values):
            values["updated_at"] = datetime.now(pytz.timezone("US/Eastern"))
            return values
