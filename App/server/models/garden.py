import uuid
from datetime import datetime
from typing import Optional
import pytz

from pydantic import BaseModel, Field, root_validator


class Garden(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    location: str = Field(...)
    config_id: str = None
    created_at: datetime = datetime.now(pytz.timezone("US/Eastern"))
    updated_at: datetime = datetime.now(pytz.timezone("US/Eastern"))

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {"name": "Og Garden", "location": "3rd Floor Endcap"}
        }

        @root_validator
        def number_validator(cls, values):
            values["updated_at"] = datetime.now(pytz.timezone("US/Eastern"))
            return values


class GardenUpdate(BaseModel):
    name: Optional[str]
    location: Optional[str]
    config_id: str = None

    class Config:
        schema_extra = {
            "example": {"name": "Don Quixote", "location": "Miguel de Cervantes"}
        }
