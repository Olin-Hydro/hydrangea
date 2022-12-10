import os
import sys
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, root_validator

parent = os.path.abspath(".")
sys.path.append(parent)

# from App.server.models.garden import Garden


class Sensor(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    garden_id: uuid.uuid4 = Field(...)
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "Humidity",
                "garden_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
            }
        }

        @root_validator
        def number_validator(cls, values):
            values["updated_at"] = datetime.utcnow()
            return values


class SensorUpdate(BaseModel):
    name: Optional[str]
    garden_id: Optional[uuid.uuid4]

    class Config:
        schema_extra = {
            "example": {
                "name": "Temp",
                "garden_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
            }
        }
