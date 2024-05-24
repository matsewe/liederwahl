from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.models as models
from app.database import get_db
from app.schemas import Song
from app.crud import get_songs_and_vote_for_session, create_or_update_vote, get_all_songs_and_votes

router = APIRouter(
    prefix="/songs",
    # dependencies=[Security(get_current_user, scopes=["public"])],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_songs(session_id: str = "", db: Annotated[Session, Depends(get_db)] = None) -> list[Song]:
    return [Song(**s.__dict__, vote=v) for s, v in get_songs_and_vote_for_session(db, session_id)]


@router.post("/{song_id}/vote")
async def vote(song_id: str, session_id: str, vote: int, db: Annotated[Session, Depends(get_db)]):
    create_or_update_vote(db, song_id, session_id, vote)


@router.get("/evaluation")
async def get_evaluation(db: Annotated[Session, Depends(get_db)] = None) -> dict[int, dict[int, int]]:
    return get_all_songs_and_votes(db)