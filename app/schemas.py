from typing import Optional
from pydantic import BaseModel


class Song(BaseModel):
    id: int
    og_artist: Optional[str]
    aca_artist: Optional[str]
    title: Optional[str]
    url: Optional[str]
    yt_id: Optional[str]
    spfy_id: Optional[str]
    thumbnail: Optional[str]
    is_aca: Optional[bool]
    arng_url: Optional[str]
    categories: Optional[dict[str, bool]]
    main_category: Optional[str]
    singable: Optional[bool]
    vote: Optional[int]
