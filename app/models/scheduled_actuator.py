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
        schema_extra = {
            "example": {
                "_id": "15a2a241-cf21-4365-af45-3d140712f2b8",
                "name": "water pump",
                "garden_id": "66608a32-a24c-4b70-ae2c-c46c586ea0c3",
                "created_at": "2023-02-17T20:19:00.545693",
                "updated_at": "2023-02-17T20:19:00.545694",
            }
        }

        @root_validator
        def number_validator(cls, values):
            values["updated_at"] = datetime.now(pytz.timezone("US/Eastern"))
            return values


class SA_Update(BaseModel):
    name: Optional[str]
    garden_id: Optional[str]

    class Config:
        schema_extra = {"example": {"name": "Don Quixote", "garden_id": "a47a4b121"}}
