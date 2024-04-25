from typing import Optional, List
import gspread
from pydantic import BaseModel

class GoogleFile(BaseModel):
    file_id: str
    file_name: str

class Genre(BaseModel):
    genre_id: Optional[int]
    genre_name: str

class Song(BaseModel):
    song_id: Optional[int]
    song_title: str
    url: str
    genres: List[Genre]