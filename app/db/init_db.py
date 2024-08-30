from sqlalchemy.orm import Session
from app import crud, schemas
from fastapi import Depends
from app.dependencies import get_db


def init_db(db: Session) -> None:
    pass