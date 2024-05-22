from fastapi import FastAPI, Request, Depends
from app.routers import admin, user, songs
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database import engine, Base, get_db
from app.crud import get_songs_and_vote_for_user
from sqlalchemy.orm import Session
from typing import Annotated
from app.schemas import Song

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(admin.router)
app.include_router(user.router)
app.include_router(songs.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request, session_id : str = "", db: Annotated[Session, Depends(get_db)] = None):
    if session_id == "":
        return templates.TemplateResponse(
            request=request, name="landing.html"
        )
    else:
        songs = [Song(**s.__dict__, vote=v) for s, v in get_songs_and_vote_for_user(db, session_id)]

        songs_by_category = {}
        all_categories = set()
        for song in songs:
            if song.main_category not in songs_by_category:
                songs_by_category[song.main_category] = []
            songs_by_category[song.main_category].append(song)
            all_categories.update(song.categories.keys())
        return templates.TemplateResponse(
            request=request, name="voting.html", context={
                "songs_by_category": songs_by_category, 
                "all_categories": {c: i+1 for i, c in enumerate(all_categories)},
                "session_id": session_id
                }
        )

#@app.get("/vote", response_class=HTMLResponse)
#async def vote(request: Request, session_id : str = ""):
#    return templates.TemplateResponse(
#        request=request, name="voting-old.html"
#    )