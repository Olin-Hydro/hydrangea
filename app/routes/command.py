from typing import List

from fastapi import APIRouter, Body, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder

from app.models.command import Command


router = APIRouter()


@router.post(
    "/",
    response_description="Create new commands",
    status_code=status.HTTP_201_CREATED,
    response_model=List[Command],
)
def create_command(request: Request, commands: List[Command] = Body(...)):
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
def list_commands(request: Request, limit: int = 1000):
    commands = list(request.app.database["commands"].find())
    commands.sort(key=lambda r: r["updated_at"], reverse=True)
    return commands[:limit]


@router.get(
    "/{id}",
    response_description="Get a single command by id",
    response_model=Command,
)
def find_command(id: str, request: Request):
    if (
        command := request.app.database["commands"].find_one({"_id": id})
    ) is not None:
        return command

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Command with ID {id} not found",
    )
