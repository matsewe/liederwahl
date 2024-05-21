from sqlalchemy import Column, String, Integer, Boolean, PickleType
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class SqlSong(Base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True)
    og_artist = Column(String)
    aca_artist = Column(String)
    title = Column(String)
    url = Column(String)
    yt_id = Column(String)
    spfy_id = Column(String)
    thumbnail = Column(String)
    is_aca = Column(Boolean)
    arng_url = Column(String)
    
    categories = Column(PickleType)

    main_category = Column(String)

    singable = Column(Boolean)

class SqlVote(Base):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True)
    song_id = Column(Integer)
    user_id = Column(String)
    vote = Column(Integer, nullable=True)