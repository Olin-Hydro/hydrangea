from datetime import datetime
from typing import Optional

from bson import ObjectId
from dotenv import load_dotenv
from pydantic import BaseModel, Field, root_validator

load_dotenv()


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class GardenModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
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