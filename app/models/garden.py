import uuid
from datetime import datetime
from typing import Optional, Union, List
import pytz

from pydantic import BaseModel, Field, field_validator
from app.models.pod import Pod, PodUpdate


class Garden(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    location: str = Field(...)
    config_id: Optional[str] = None
    pods: Optional[List[Pod]] = None
    created_at: datetime = datetime.now(pytz.timezone("US/Eastern"))
    updated_at: datetime = datetime.now(pytz.timezone("US/Eastern"))

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "66608a32-a24c-4b70-ae2c-c46c586ea0c3",
                "name": "Og Garden",
                "location": "3rd Floor Endcap",
                "config_id": "77608a32-a45c-4b70-ae2c-c46c586ea0c3",
                "pods": [
                    {
                        "_id": "66608a32-a24c-4b70-ae2c-c46c586ea0c3",
                        "name": "Johns Lettuce",
                        "garden_id": "77608a32-a45c-4b70-ae2c-c46c586ea0c3",
                        "location": [1, 3],
                        "plant": "Lettuce",
                        "created_at": "2023-02-17T20:19:00.536083",
                        "updated_at": "2023-02-17T20:19:00.536084",
                    }
                ],
                "created_at": "2023-02-17T20:19:00.536083",
                "updated_at": "2023-02-17T20:19:00.536084",
            }
        }

        @field_validator("updated_at")
        def number_validator(cls, values):
            values["updated_at"] = datetime.now(pytz.timezone("US/Eastern"))
            return values


class GardenUpdate(BaseModel):
    name: Optional[str]
    location: Optional[str]
    config_id: Optional[str]
    pods: Union[List[Pod], List[PodUpdate], None]
    updated_at: datetime = datetime.now(pytz.timezone("US/Eastern"))

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Don Quixote",
                "location": "Miguel de Cervantes",
                "config_id": "abcd",
                "pods": [
                    {
                        "_id": "66608a32-a24c-4b70-ae2c-c46c586ea0c3",
                        "name": "Johns Lettuce",
                        "garden_id": "77608a32-a45c-4b70-ae2c-c46c586ea0c3",
                        "location": [1, 3],
                        "plant": "Lettuce",
                        "created_at": "2023-02-17T20:19:00.536083",
                        "updated_at": "2023-02-17T20:19:00.536084",
                    }
                ],
            }
        }
