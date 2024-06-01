from typing import Annotated
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

import app.models as models
from app.database import get_db
from app.schemas import Song
import app.crud as crud

router = APIRouter(
    prefix="/session",
    # dependencies=[Security(get_current_user, scopes=["public"])],
    responses={404: {"description": "Not found"}},
)


@router.put("/{session_id}")
async def activate_session(session_id: str = "", db: Annotated[Session, Depends(get_db)] = None):
    crud.activate_session(db, session_id)

@router.delete("/{session_id}")
async def deactivate_session(session_id: str = "", db: Annotated[Session, Depends(get_db)] = None):
    crud.deactivate_session(db, session_id)

#@router.get("/{session_id}")
#async def get_session(session_id: str = "", db: Annotated[Session, Depends(get_db)] = None):
#    return "get " + session_id