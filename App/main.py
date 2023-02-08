import os

import uvicorn

from dotenv import load_dotenv

load_dotenv()

port = int(os.environ["PORT"])

if __name__ == "__main__":
    uvicorn.run("server.app:app", host="0.0.0.0", port=port, reload=False)
