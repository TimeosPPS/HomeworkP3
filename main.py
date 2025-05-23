from typing import Optional
from fastapi import FastAPI, Header, Path, Query
from fastapi.concurrency import asynccontextmanager
from datetime import datetime
from pydantic import BaseModel
import uvicorn

from models import database

class ResponseModel(BaseModel):
    user_id: int
    timestamp: datetime
    x_client_version: str
    message: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

@app.get("/users/{user_id}", response_model=ResponseModel)
async def get_user_info(
    user_id: int = Path(..., description="User ID"),
    timestamp: Optional[datetime] = Query(None, description="Timestamp"),
    x_client_version: str = Header(..., alias="X-Client-Version")
):
    if timestamp is None:
        timestamp = datetime.utcnow()
    
    return {
        "user_id": user_id,
        "timestamp": timestamp,
        "x_client_version": x_client_version,
        "message": f"Hello, user {user_id}!"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
