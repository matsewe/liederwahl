from fastapi import FastAPI, Request, Depends
from app.routers import admin, user, songs, session
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database import engine, Base, get_db, SessionLocal
from app.crud import get_songs_and_vote_for_session, get_setting
from sqlalchemy.orm import Session
from typing import Annotated
from app.schemas import Song
import json
import os
import asyncio

from starlette.middleware import Middleware

from starlette_context import context, plugins
from starlette_context.middleware import RawContextMiddleware

if os.path.isfile("first_run") and os.environ.get("RELOAD_ON_FIRST_RUN"):
    print("First run ... load data")
    with SessionLocal() as db:
        asyncio.run(admin.create_upload_file(include_non_singable=True, db=db))
    os.remove("first_run")

#Base.metadata.create_all(engine)

middleware = [
    Middleware(
        RawContextMiddleware,
        plugins=(
            plugins.ForwardedForPlugin(),
            plugins.UserAgentPlugin()
        )
    )
]

app = FastAPI(middleware=middleware)

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
async def vote(request: Request, session_id: str, db: Session = Depends(get_db)) -> HTMLResponse:
    veto_mode = get_setting(db, "veto_mode")

    songs = [Song(**s.__dict__, vote=v, vote_comment=c)
             for s, v, c in get_songs_and_vote_for_session(db, session_id)]

    songs_by_category = {}
    all_categories = set()

    wildcard_songs = []
    current_songs = []
    other_songs = []

    for song in songs:
        if (not song.singable) and (not veto_mode):
            continue

        if song.is_current:
            current_songs.append(song)
            continue

        if not song.is_aca:
            wildcard_songs.append(song)
            continue

        if not song.main_category:
            other_songs.append(song)
            continue

        if song.main_category not in songs_by_category:
            songs_by_category[song.main_category] = []
        songs_by_category[song.main_category].append(song)
        all_categories.update(song.categories.keys())

    songs_by_category["Sonstige"] = other_songs
    songs_by_category["Wildcard (nicht a cappella)"] = wildcard_songs
    songs_by_category["Aktuelles Programm"] = current_songs

    all_categories = list(all_categories)
    all_categories.sort()

    all_categories.append("Sonstige")
    all_categories.append("Wildcard (nicht a cappella)")
    all_categories.append("Aktuelles Programm")

    # print(all_categories)
    # with open('/data/songs_by_cat.json', 'w') as f:
    #    json.dump({cat : [s.__dict__ for s in songs] for cat, songs in songs_by_category.items()}, f)

    return templates.TemplateResponse(
        request=request, name="voting.html", context={
            "songs_by_category": songs_by_category,
            "all_categories": {c: i+1 for i, c in enumerate(all_categories)},
            "session_id": session_id,
            "veto_mode": veto_mode
        }
    )
