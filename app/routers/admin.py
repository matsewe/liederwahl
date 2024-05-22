import pandas as pd
import numpy as np
import re
import requests
import os
from fastapi import APIRouter, Security, Depends
from sqlalchemy.orm import Session

from app.database import get_db, engine, Base
from app.routers.user import get_current_user
from app.crud import create_song

router = APIRouter(
    prefix="/admin",
    dependencies=[Security(get_current_user, scopes=["admin"])],
    responses={404: {"description": "Not found"}},
)


def get_main_category(categories) -> int:
    if np.sum(categories != None) == 1:
        return np.argmax(categories != None, axis=0)
    elif "h" in categories:
        return np.argmax(categories == "h", axis=0)
    else:
        return np.argmax(categories != None, axis=0)


def get_youtube_id(url):
    if url is None:
        return None

    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        return youtube_regex_match.group(6)

    return None


def get_thumbnail(url):
    if url is None:
        return "/static/cover.jpg"

    m = get_youtube_id(url)
    if m:
        thumbnail_url = "https://img.youtube.com/vi/" + m + "/mqdefault.jpg"
        return thumbnail_url
    elif "spotify" in url:
        return re.findall(r'(https?://i.scdn.co/image[^"]+)', requests.get(url).text)[0]
    else:
        return "/static/cover.jpg"


def get_spotify_id(url):
    if url is None:
        return None
    if "spotify" in url:
        return url.split("/track/")[1]
    else:
        return None


@router.post("/load_list")
async def create_upload_file(db: Session = Depends(get_db)):

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    song_list = pd.read_excel(os.environ['LIST_URL'])
    song_list = song_list.replace({np.nan: None})
    song_list = song_list.replace({"n/a": None})

    category_names = list(song_list.iloc[0][6:19])

    for row in song_list[1:].iterrows():
        row = np.array(row[1])

        yt_id = get_youtube_id(row[3])
        spfy_id = get_spotify_id(row[3])

        categories = {n: v for n, v in zip(
            category_names, row[6:19] != None)}

        if not np.any(list(categories.values())):
            continue

        create_song(db,
                    og_artist=row[0],
                    aca_artist=row[1],
                    title=row[2],
                    url=row[3],
                    yt_id=yt_id,
                    spfy_id=spfy_id,
                    thumbnail=get_thumbnail(row[3]),
                    is_aca=row[4] == "ja",
                    arng_url=row[5],
                    categories=categories,
                    main_category=category_names[get_main_category(row[6:19])],
                    singable=row[19] != "nein"
                    )
