import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, root_validator


class Reactive_Actuator(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    sensor_id: str = Field(...)
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Config:
        allow_population_by_field_name = True
        schema_extra = {"example": {"name": "nutrient pump", "sensor_id": "id number"}}

        @root_validator
        def number_validator(cls, values):
            values["updated_at"] = datetime.utcnow()
            return values


class RA_Update(BaseModel):
    name: Optional[str]

    class Config:
        schema_extra = {"example": {"name": "Don Quixote", "sensor_id": "a47a4b121"}}
