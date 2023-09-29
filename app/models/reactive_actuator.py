import uuid
import pytz
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Reactive_Actuator(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    sensor_id: str = Field(...)
    created_at: datetime = datetime.now(pytz.timezone("US/Eastern"))
    updated_at: datetime = datetime.now(pytz.timezone("US/Eastern"))

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "5e9b44c7-970a-41f0-8ef4-e4dbf82f00c3",
                "name": "ph down pump",
                "sensor_id": "5ff70c48-7a56-47fe-b7d9-8df3be3e3197",
                "created_at": "2023-02-17T20:19:00.549263",
                "updated_at": "2023-02-17T20:19:00.549264",
            }
        }

        @field_validator("updated_at")
        def number_validator(cls, values):
            values["updated_at"] = datetime.now(pytz.timezone("US/Eastern"))
            return values


class RA_Update(BaseModel):
    name: Optional[str]
    sensor_id: Optional[str]
    updated_at: datetime = datetime.now(pytz.timezone("US/Eastern"))

    class Config:
        json_schema_extra = {
            "example": {"name": "Don Quixote", "sensor_id": "a47a4b121"}
        }
