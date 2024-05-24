from fastapi import FastAPI, Request, Depends
from app.routers import admin, user, songs, session
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database import engine, Base, get_db
from app.crud import get_songs_and_vote_for_session
from sqlalchemy.orm import Session
from typing import Annotated
from app.schemas import Song

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(admin.router)
app.include_router(user.router)
app.include_router(songs.router)
app.include_router(session.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request, name="landing.html"
    )


@app.get("/vote")
async def vote(request: Request, session_id: str, db: Annotated[Session, Depends(get_db)]) -> HTMLResponse:
    songs = [Song(**s.__dict__, vote=v)
             for s, v in get_songs_and_vote_for_session(db, session_id)]

    songs_by_category = {}
    all_categories = set()

    wildcard_songs = []

    for song in songs:
        if not song.is_aca:
            wildcard_songs.append(song)
            continue

        if song.main_category not in songs_by_category:
            songs_by_category[song.main_category] = []
        songs_by_category[song.main_category].append(song)
        all_categories.update(song.categories.keys())

    songs_by_category["Wildcard (nicht a cappella)"] = wildcard_songs

    all_categories = list(all_categories)
    all_categories.sort()

    all_categories.append("Wildcard (nicht a cappella)")

    print(all_categories)

    return templates.TemplateResponse(
        request=request, name="voting.html", context={
            "songs_by_category": songs_by_category,
            "all_categories": {c: i+1 for i, c in enumerate(all_categories)},
            "session_id": session_id
        }
    )
