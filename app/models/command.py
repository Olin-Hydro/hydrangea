"""
The code defines two Pydantic data models, 'Command' and 'CommandUpdate,' for representing and 
managing commands and their updates, including fields for identifiers, timestamps, and execution status. 
It ensures data validation and maintains up-to-date timestamps for command updates using Pydantic's 
configuration and validation capabilities. 
"""

import uuid  # Import the 'uuid' module to generate unique identifiers.
from datetime import datetime  # Import 'datetime' for working with timestamps.
import pytz  # Import 'pytz' for timezone support.
from pydantic import BaseModel, Field, root_validator  # Import Pydantic components.

# Define a Pydantic data model 'Command' for representing a command.
class Command(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")  # Unique identifier for the command.
    ref_id: str = Field(...)  # Reference identifier for the command.
    cmd: int = Field(...)  # The command code.
    type: str = Field(...)  # The type of command.
    executed: str = Field(default="false")  # Flag indicating whether the command has been executed.
    garden_id: str = Field(...)  # Identifier of the associated garden.
    created_at: datetime = datetime.now(pytz.timezone("US/Eastern"))  # Timestamp for command creation.
    updated_at: datetime = datetime.now(pytz.timezone("US/Eastern"))  # Timestamp for command updates.

    class Config:
        allow_population_by_field_name = True  # Allow populating model fields using dictionary keys.

        schema_extra = {
            "example": {
                "_id": "66608a32-a24c-4b70-ae2c-c46c586ea0c3",
                "ref_id": "36708a32-a24c-4b70-ae2c-c46c586ea0c3",
                "cmd": 1,
                "type": "reactive actuator",
                "executed": "false",
                "garden_id": "87808a32-a24c-4b70-ae2c-c46c586ea0c3",
                "created_at": "2023-02-17T20:19:00.536083",
                "updated_at": "2023-02-17T20:19:00.536084",
            }
        }  # Example data structure for documentation.

        @root_validator
        def number_validator(cls, values):
            # Ensure 'updated_at' field is updated when any values change.
            values["updated_at"] = datetime.now(pytz.timezone("US/Eastern"))
            return values

# Define a Pydantic data model 'CommandUpdate' for updating command execution status.
class CommandUpdate(BaseModel):
    executed: str  # New execution status for the command.
    updated_at: datetime = datetime.now(pytz.timezone("US/Eastern"))  # Timestamp for update.

    class Config:
        schema_extra = {"example": {"executed": "true"}}  # Example data structure for documentation.
