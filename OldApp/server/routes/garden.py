import os
import sys
<<<<<<< HEAD:app/server/routes/garden.py
from dotenv import load_dotenv
from fastapi import APIRouter, Body, status, HTTPException, Depends, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List
from fastapi.responses import JSONResponse, Response
from server.models.garden import GardenModel, UpdateGardenModel
from server.database import db
from server.models.user import User, UserInDB
=======
from typing import List
>>>>>>> 2218764bb74fa1b6ca9168623c52da16ab520314:OldApp/server/routes/garden.py

from dotenv import load_dotenv
from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

parent = os.path.abspath(".")
sys.path.append(parent)
from OldApp.server.database import db
from OldApp.server.models.garden import GardenModel, UpdateGardenModel

load_dotenv()

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

router = APIRouter()

def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post("/", response_description="Add new garden", response_model=GardenModel)
async def create_garden(garden: GardenModel = Body(...)):
    garden = jsonable_encoder(garden)
    new_garden = await db["gardens"].insert_one(garden)
    created_garden = await db["gardens"].find_one({"_id": new_garden.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_garden)



@router.get(
    "/", response_description="List all gardens", response_model=List[GardenModel]
)
async def list_gardens():
    gardens = await db["gardens"].find().to_list(1000)
    return gardens


@router.get(
    "/{id}", response_description="Get a single garden", response_model=GardenModel
)
async def show_garden(id: str):
    if (garden := await db["gardens"].find_one({"_id": id})) is not None:
        return garden

    raise HTTPException(status_code=404, detail=f"Garden {id} not found")


@router.put("/{id}", response_description="Update a garden", response_model=GardenModel)
async def update_garden(id: str, garden: UpdateGardenModel = Body(...)):
    garden = {k: v for k, v in garden.dict().items() if v is not None}

    if len(garden) >= 1:
        update_result = await db["gardens"].update_one({"_id": id}, {"$set": garden})

        if update_result.modified_count == 1:
            if (
                updated_garden := await db["gardens"].find_one({"_id": id})
            ) is not None:
                return updated_garden

    if (existing_garden := await db["gardens"].find_one({"_id": id})) is not None:
        return existing_garden

    raise HTTPException(status_code=404, detail=f"Garden {id} not found")
