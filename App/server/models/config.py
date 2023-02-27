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
                "_id": "b67cd1cf-e113-40cf-a293-ba80251e03ce",
                "name": "TestConfig",
                "sensor_schedule": [
                    {
                        "sensor_id": "66608a32-a24c-4b70-ae2c-c46c586ea0c3",
                        "interval": 300.0,
                    }
                ],
                "ra_schedule": [
                    {
                        "ra_id": "5e9b44c7-970a-41f0-8ef4-e4dbf82f00c3",
                        "interval": 1200.0,
                        "threshold": 7.5,
                        "duration": 5.0,
                        "threshold_type": 1,
                    }
                ],
                "sa_schedule": [
                    {
                        "sa_id": "15a2a241-cf21-4365-af45-3d140712f2b8",
                        "on": [
                            "2023-02-17T08:09:50+00:00",
                            "2023-02-17T16:09:50+00:00",
                            "2023-02-17T20:09:50+00:00",
                        ],
                        "off": [
                            "2023-02-17T08:29:50+00:00",
                            "2023-02-17T16:29:50+00:00",
                            "2023-02-17T20:29:50+00:00",
                        ],
                    }
                ],
                "created_at": "2023-02-18T21:15:12.005399",
                "updated_at": "2023-02-18T21:15:12.005400",
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
