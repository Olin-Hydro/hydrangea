import uuid
import pytz
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, root_validator


class Scheduled_Actuator(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    garden_id: str = Field(...)
    created_at: datetime = datetime.now(pytz.timezone("US/Eastern"))
    updated_at: datetime = datetime.now(pytz.timezone("US/Eastern"))

    class Config:
        allow_population_by_field_name = True
        schema_extra = {"example": {"name": "water pump", "garden_id": "id number"}}

        @root_validator
        def number_validator(cls, values):
            values["updated_at"] = datetime.now(pytz.timezone("US/Eastern"))
            return values


class SA_Update(BaseModel):
    name: Optional[str]

    class Config:
        schema_extra = {"example": {"name": "Don Quixote", "garden_id": "a47a4b121"}}
