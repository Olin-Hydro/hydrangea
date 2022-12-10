import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, root_validator


class Garden(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    location: str = Field(...)
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {"name": "Og Garden", "location": "3rd Floor Endcap"}
        }

        @root_validator
        def number_validator(cls, values):
            values["updated_at"] = datetime.utcnow()
            return values


class GardenUpdate(BaseModel):
    name: Optional[str]
    location: Optional[str]

    class Config:
        schema_extra = {
            "example": {"name": "Don Quixote", "location": "Miguel de Cervantes"}
        }
