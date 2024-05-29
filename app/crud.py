import app.models as models
from sqlalchemy import func
from sqlalchemy.orm.attributes import flag_modified


def get_songs_and_vote_for_session(db, session_name) -> list[models.Song]:
    session_entry = activate_session(db, session_name)

    votes = db.query(models.Vote).filter(
        models.Vote.session_id == session_entry.id).subquery()

    songs_and_votes = db.query(
        models.Song, votes.c.vote, votes.c.comment
    ).join(votes, isouter=True).filter().all()

    return songs_and_votes


def get_all_songs_and_votes(db) -> dict[int, dict[int, int]]:
    _v = db.query(models.Vote.song_id, models.Vote.vote, func.count(
        models.Vote.song_id)).group_by(models.Vote.song_id, models.Vote.vote).all()

    votes = {}

    for v in _v:
        if v[0] not in votes:
            votes[v[0]] = {-1: 0, 0: 0, 1: 0}
        votes[v[0]][v[1]] = v[2]

    return votes


def create_song(db,
                og_artist,
                aca_artist,
                title,
                url,
                source,
                yt_id,
                spfy_id,
                thumbnail,
                is_current,
                is_aca,
                arng_url,
                categories,
                main_category,
                singable,
                comment
                ):
    s = models.Song(og_artist=og_artist,
                    aca_artist=aca_artist,
                    title=title,
                    url=url,
                    source=source,
                    yt_id=yt_id,
                    spfy_id=spfy_id,
                    thumbnail=thumbnail,
                    is_current=is_current,
                    is_aca=is_aca,
                    arng_url=arng_url,
                    categories=categories,
                    main_category=main_category,
                    singable=singable,
                    comment=comment)

    db.add(s)
    db.commit()


def create_or_update_vote(db, song_id, session_name, vote):
    session_entry = activate_session(db, session_name)

    vote_entry = db.query(models.Vote).filter(
        (models.Vote.session_id == session_entry.id) & (models.Vote.song_id == song_id)).first()
    if vote_entry:
        vote_entry.vote = str(vote)  # type: ignore
    else:
        vote_entry = models.Vote(
            song_id=song_id, session_id=session_entry.id, vote=vote)
        db.add(vote_entry)
    db.commit()

def create_or_update_comment(db, song_id, session_name, comment):
    session_entry = activate_session(db, session_name)

    if comment == "":
        comment = None

    vote_entry = db.query(models.Vote).filter(
        (models.Vote.session_id == session_entry.id) & (models.Vote.song_id == song_id)).first()
    if vote_entry:
        vote_entry.comment = comment  # type: ignore
    else:
        vote_entry = models.Vote(
            song_id=song_id, session_id=session_entry.id, comment=comment)
        db.add(vote_entry)
    db.commit()

def activate_session(db, session_name):
    session_entry = db.query(models.Session).filter(
        (models.Session.session_name == session_name)).first()
    if session_entry:
        session_entry.active = True
    else:
        session_entry = models.Session(session_name=session_name, active=True)
        db.add(session_entry)
    flag_modified(session_entry, "active")
    db.commit()

    return session_entry


def deactivate_session(db, session_name):
    session_entry = db.query(models.Session).filter(
        (models.Session.session_name == session_name)).first()
    if session_entry:
        session_entry.active = False
    else:
        session_entry = models.Session(session_name=session_name, active=False)
        db.add(session_entry)
    db.commit()


def get_setting(db, key):
    entry = db.query(models.Config.value).filter(models.Config.key == key).first()
    if entry:
        return entry[0]
    else:
        return None

def set_setting(db, key, value):
    setting_entry = db.query(models.Config).filter(models.Config.key == key).first()
    if setting_entry:
        setting_entry.value = value
    else:
        setting_entry = models.Config(key=key, value=value)
        db.add(setting_entry)
    db.commit()