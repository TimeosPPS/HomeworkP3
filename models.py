from typing import List, Union, Optional

import os
from sqlalchemy import String, create_engine
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from databases import Database
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
SQLALCHEMY_URI = os.getenv("SQLALCHEMY_URI")
engine = create_engine(SQLALCHEMY_URI)
database = Database(SQLALCHEMY_URI)

Base = DeclarativeBase

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[Optional[str]] = mapped_column(datetime, default=datetime.utcnow)
    x_client_version: Mapped[str] = mapped_column(String(50))

# Base.metadata.create_all(bind=engine)
