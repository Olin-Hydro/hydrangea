"""
    This FastAPI code defines a set of API routes for managing commands in a database, 
    including creation, listing, retrieval by ID, and updates. It utilizes data models 
    and responds with appropriate status codes, enabling the interaction with command 
    data in a web application.
"""

from typing import List  # Import 'List' for type hinting.
from fastapi import APIRouter, Body, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder

from app.models.command import Command, CommandUpdate  # Import data models.

router = APIRouter()  # Create an instance of APIRouter to define route handlers.

@router.post(
    "/",
    response_description="Create new commands",
    status_code=status.HTTP_201_CREATED,
    response_model=List[Command],
)
def create_command(request: Request, commands: List[Command] = Body(...)):
    """
    Create multiple commands in the database.

    Args:
        request (Request): The FastAPI request object.
        commands (List[Command]): List of commands to create.

    Returns:
        List[Command]: List of created commands.
    """
    created_cmds = []
    for command in commands:
        cmd = jsonable_encoder(command)
        new_cmd = request.app.database["commands"].insert_one(cmd)
        created_cmd = request.app.database["commands"].find_one(
            {"_id": new_cmd.inserted_id}
        )
        created_cmds.append(created_cmd)
    return created_cmds

@router.get(
    "/", response_description="List commands", response_model=List[Command]
)
def list_commands(request: Request, limit: int = 1000, executed="false"):
    """
    List commands from the database.

    Args:
        request (Request): The FastAPI request object.
        limit (int): Maximum number of commands to retrieve.
        executed (str): Filter commands by execution status ("true" or "false").

    Returns:
        List[Command]: List of commands that match the filter criteria.
    """
    commands = list(
        request.app.database["commands"].find({"executed": executed})
    )
    commands.sort(key=lambda r: r["updated_at"], reverse=True)
    return commands[:limit]

@router.get(
    "/{id}",
    response_description="Get a single command by id",
    response_model=Command,
)
def find_command(id: str, request: Request):
    """
    Retrieve a single command by its ID from the database.

    Args:
        id (str): The ID of the command to retrieve.
        request (Request): The FastAPI request object.

    Returns:
        Command: The retrieved command.

    Raises:
        HTTPException: If the command with the specified ID is not found.
    """
    if (
        command := request.app.database["commands"].find_one({"_id": id})
    ) is not None:
        return command

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Command with ID {id} not found",
    )

@router.put(
    "/{id}", response_description="Update a command", response_model=Command
)
def update_command(id: str, request: Request, cmd: CommandUpdate = Body(...)):
    """
    Update a command in the database.

    Args:
        id (str): The ID of the command to update.
        request (Request): The FastAPI request object.
        cmd (CommandUpdate): The updated command data.

    Returns:
        Command: The updated command.

    Raises:
        HTTPException: If the command with the specified ID is not found.
    """
    cmd = {k: v for k, v in cmd.dict().items() if v is not None}

    if len(cmd) >= 2:
        update_result = request.app.database["commands"].update_one(
            {"_id": id}, {"$set": cmd}
        )

        if update_result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nothing was updated",
            )

    if (
        existing_cmd := request.app.database["commands"].find_one({"_id": id})
    ) is not None:
        return existing_cmd

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Command with ID {id} not found",
    )
