from typing import Optional, List
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from datetime import datetime
from pydantic import BaseModel, Field
import uvicorn

from models import User, database
from sqlalchemy import insert, select

class UserModel(BaseModel):
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)
    xClientVersion: str


class UserModeLResponse(UserModel):
    user_id: int

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

@app.get("/users/", response_model=List[UserModeLResponse])
async def get_users():
    query = select(User)
    users = await database.fetch_all(query)
    return f"Hello! {users}"

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
