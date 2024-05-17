from fastapi import APIRouter, HTTPException, Security
from app.models import Song
from app.sql_models import SqlSong, SqlVote
from app.dependencies import session
from app.routers.user import get_current_user, User
from typing import Annotated

router = APIRouter(
    prefix="/songs",
    #dependencies=[Security(get_current_user, scopes=["public"])],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def get_songs(user_id : str = "") -> list[Song]:
    sqlsongs = session.query(SqlSong).filter(SqlSong.singable == True).all()
    votes = session.query(SqlVote).filter(SqlVote.user_id == user_id).all()
    votes = {v.song_id : v.vote for v in votes}

    return [Song(**s.__dict__, vote=votes.get(s.id, None)) for s in sqlsongs] # type: ignore

@router.post("/{song_id}/vote")
async def vote(song_id : str, user_id : str, vote : int):
    vote_entry = session.query(SqlVote).filter((SqlVote.user_id == user_id) & (SqlVote.song_id == song_id)).first()
    if vote_entry:
        vote_entry.vote = str(vote) # type: ignore
    else:
        vote_entry = SqlVote(song_id=song_id, user_id=user_id, vote=vote)
        session.add(vote_entry)
    session.commit()
