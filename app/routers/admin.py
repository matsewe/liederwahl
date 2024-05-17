from fastapi import APIRouter, Security
from app.sql_models import SqlSong
from app.dependencies import session
from app.routers.user import get_current_user
import pandas as pd
import numpy as np

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


@router.post("/process_file")
async def create_upload_file(link_share: str):
    song_list = pd.read_excel(link_share)
    song_list = song_list.replace({np.nan: None})
    song_list = song_list.replace({"n/a": None})

    category_names = list(song_list.iloc[0][6:19])

    for row in song_list[1:].iterrows():
        row = np.array(row[1])

        s = SqlSong(og_artist=row[0],
                    aca_artist=row[1],
                    title=row[2],
                    yt_url=row[3],
                    is_aca=row[4] == "ja",
                    arng_url=row[5],
                    categories={n: v for n, v in zip(
                        category_names, row[6:19] != None)},
                    main_category=category_names[get_main_category(row[6:19])],
                    singable=row[19] != "nein"
                    )

        session.add(s)
        session.commit()
