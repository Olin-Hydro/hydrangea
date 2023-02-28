import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, root_validator


class SASchedule(BaseModel):
    sa_id: str = Field(...)
    on: List[datetime] = Field(...)
    off: List[datetime] = Field(...)


class SensorSchedule(BaseModel):
    sensor_id: str = Field(...)
    interval: float = Field(...)


class RASchedule(BaseModel):
    ra_id: str = Field(...)
    interval: float = Field(...)
    threshold: float = Field(...)
    duration: float = Field(...)
    threshold_type: int = Field(...)


class Config(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    sensor_schedule: List[SensorSchedule] = Field(...)
    ra_schedule: List[RASchedule] = Field(...)
    sa_schedule: List[SASchedule] = Field(...)
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "Config",
                "sensor_schedule": [{"sensor_id": "abc", "interval": 300}],
                "ra_schedule": [
                    {
                        "ra_id": "bcd",
                        "interval": 1200,
                        "threshold": 7.5,
                        "duration": 5,
                        "threshold_type": 0,
                    }
                ],
                "sa_schedule": [
                    {
                        "sa_id": "ccd",
                        "on": [
                            "2023-02-17T08:09:50+0000",
                            "2023-02-17T16:09:50+0000",
                            "2023-02-17T20:09:50+0000",
                        ],
                        "off": [
                            "2023-02-17T08:29:50+0000",
                            "2023-02-17T16:29:50+0000",
                            "2023-02-17T20:29:50+0000",
                        ],
                    }
                ],
            }
        }

        @root_validator
        def number_validator(cls, values):
            values["updated_at"] = datetime.utcnow()
            return values


class ConfigUpdate(BaseModel):
    name: Optional[str]
    sensor_schedule: Optional[List[SensorSchedule]]
    ra_schedule: Optional[List[RASchedule]]
    sa_schedule: Optional[List[SASchedule]]

    class Config:
        schema_extra = {
            "example": {
                "name": "Config 1",
                "sensor_schedule": [{"sensor_id": "abc", "interval": 400}],
            }
        }
