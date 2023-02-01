import os

import uvicorn

# import sys
from dotenv import load_dotenv

load_dotenv()
# from dotenv import dotenv_values

# load environment variables
port = int(os.environ["PORT"])

if __name__ == "__main__":
    uvicorn.run("server.app:app", host="0.0.0.0", port=port, reload=False)
