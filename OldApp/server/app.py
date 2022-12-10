import os
import sys

from fastapi import FastAPI

parent = os.path.abspath(".")
sys.path.append(parent)

# from App.server.routes.config import router as ConfigRouter
from App.server.routes.garden import router as GardenRouter

# from App.server.routes.ra import router as RARouter
# from App.server.routes.sa import router as SARouter
# from App.server.routes.sensor import router as SensorRouter

app = FastAPI()

app.include_router(GardenRouter, tags=["Garden"], prefix="/Garden")

# app.include_router(SensorRouter, tags=["Sensor"], prefix="/Sensor")

# app.include_router(RARouter, tags=["RA"], prefix="/RA")

# app.include_router(SARouter, tags=["SA"], prefix="/SA")

# app.include_router(ConfigRouter, tags=["Config"], prefix="/Config")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the 2022-23 Hydro API!"}
