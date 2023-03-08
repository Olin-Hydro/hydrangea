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
            "example": {
                "_id": "66608a32-a24c-4b70-ae2c-c46c586ea0c3",
                "cmd": 1,
                "type": "reactive actuator",
                "garden_id": "87808a32-a24c-4b70-ae2c-c46c586ea0c3",
                "created_at": "2023-02-17T20:19:00.536083",
                "updated_at": "2023-02-17T20:19:00.536084",
            }
        }

        @root_validator
        def number_validator(cls, values):
            values["updated_at"] = datetime.now(pytz.timezone("US/Eastern"))
            return values
