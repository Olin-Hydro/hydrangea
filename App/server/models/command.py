import uuid
from datetime import datetime

from pydantic import BaseModel, Field, root_validator
import pytz


class Command(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    cmd: int = Field(...)
    type: str = Field(...)
    garden_id: str = Field(...)
    created_at: datetime = datetime.now(pytz.timezone("US/Eastern"))
    updated_at: datetime = datetime.now(pytz.timezone("US/Eastern"))

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {"cmd": 1, "type": "reactive actuator", "garden_id": "abc"}
        }

        @root_validator
        def number_validator(cls, values):
            values["updated_at"] = datetime.now(pytz.timezone("US/Eastern"))
            return values
