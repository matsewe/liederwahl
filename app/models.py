from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.sql import func
from typing import Optional
from datetime import datetime


class Song(Base):
    __tablename__ = 'songs'
    id: Mapped[int] = mapped_column(primary_key=True)
    og_artist: Mapped[Optional[str]]
    aca_artist: Mapped[Optional[str]]
    title: Mapped[Optional[str]]
    url: Mapped[Optional[str]]
    source: Mapped[Optional[str]]
    yt_id: Mapped[Optional[str]]
    spfy_id: Mapped[Optional[str]]
    thumbnail: Mapped[Optional[str]]
    is_current: Mapped[Optional[bool]]
    is_aca: Mapped[Optional[bool]]
    arng_url: Mapped[Optional[str]]
    categories: Mapped[Optional[dict[str, bool]]]
    main_category: Mapped[Optional[str]]
    singable: Mapped[Optional[bool]]


class Session(Base):
    __tablename__ = 'sessions'
    id: Mapped[int] = mapped_column(primary_key=True)
    session_name: Mapped[int]
    active: Mapped[bool]
    time_created: Mapped[datetime] = mapped_column(server_default=func.now())
    time_updated: Mapped[Optional[datetime]
                         ] = mapped_column(onupdate=func.now())


class Vote(Base):
    __tablename__ = 'votes'
    id: Mapped[int] = mapped_column(primary_key=True)
    song_id: Mapped[int] = mapped_column(Integer, ForeignKey("songs.id"))
    session_id: Mapped[int] = mapped_column(Integer, ForeignKey("sessions.id"))
    vote: Mapped[Optional[int]]
    time_created: Mapped[datetime] = mapped_column(server_default=func.now())
    time_updated: Mapped[Optional[datetime]
                         ] = mapped_column(onupdate=func.now())
