import os
import sys
from datetime import datetime
from typing import Optional

from bson import ObjectId

parent = os.path.abspath(".")
sys.path.append(parent)

# print(sys.path)
from dotenv import load_dotenv
from pydantic import BaseModel, Field, root_validator

from OldApp.server.models.id import PyObjectId

load_dotenv()


class GardenModel(BaseModel):
    id: PyObjectId = Field(alias="_id")
    name: str = Field(...)
    location: str = Field(...)
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        validate_assignment = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {"name": "OG Garden", "location": "3rd Floor Endcap"}
        }

        @root_validator
        def number_validator(cls, values):
            values["updated_at"] = datetime.now()
            return values


class UpdateGardenModel(BaseModel):
    name: Optional[str]
    location: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {"example": {"name": "OG", "locaiton": "Cafeteria"}}
