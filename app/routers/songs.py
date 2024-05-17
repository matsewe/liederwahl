from fastapi import APIRouter, HTTPException, Security
from app.models import Song
from app.dependencies import dbEngine, Base, dbSession
from app.routers.user import get_current_user, User
from typing import Annotated

router = APIRouter(
    prefix="/songs",
    #dependencies=[Security(get_current_user, scopes=["public"])],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_songs() -> list[dict]:
    return dbSession.query(Base.songs).all()
