import os
import sys
from datetime import datetime
from typing import Union

parent = os.path.abspath(".")
sys.path.append(parent)

from bson import ObjectId
from dotenv import load_dotenv
from pydantic import BaseModel, Field, root_validator

from OldApp.server.models.id import PyObjectId

load_dotenv()


class ScheduledActuatorModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    garden_id: Union[PyObjectId, None] = Field(default=None, alias="garden_id")
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        validate_assignment = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {"name": "Water pump", "garden_id": "6359d55bff77b777dd5c92e8"}
        }

        @root_validator
        def number_validator(cls, values):
            values["updated_at"] = datetime.now()
            return values
