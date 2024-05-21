from typing import Optional
from pydantic import BaseModel

class GoogleFile(BaseModel):
    file_id: str
    file_name: str

class Genre(BaseModel):
    genre_id: Optional[int]
    genre_name: str

class Song(BaseModel):
    id: int
    og_artist: Optional[str]
    aca_artist: Optional[str]
    title: Optional[str]
    url: Optional[str]
    yt_id: Optional[str]
    spfy_id: Optional[str]
    thumbnail: Optional[str]
    is_aca: bool
    arng_url: Optional[str]
    categories: dict[str, bool]
    main_category: str
    singable: bool
    vote: Optional[int]