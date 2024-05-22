import app.models as models
from sqlalchemy import func

def get_songs_and_vote_for_user(db, user_id) -> list[models.Song]:
    votes = db.query(models.Vote).filter(models.Vote.user_id == user_id).subquery()

    songs_and_votes = db.query(
        models.Song, votes.c.vote
    ).filter(
        models.Song.singable == True
    ).join(votes, isouter=True).filter().all()

    return songs_and_votes


def get_all_songs_and_votes(db) -> dict[int, dict[int, int]]:
    _v = db.query(models.Vote.song_id, models.Vote.vote, func.count(models.Vote.song_id)).group_by(models.Vote.song_id, models.Vote.vote).all()

    votes = {}

    for v in _v:
        if v[0] not in votes:
            votes[v[0]] = {-1 : 0, 0 : 0, 1 : 0}
        votes[v[0]][v[1]] = v[2]

    return votes

def create_song(db,
                og_artist,
                aca_artist,
                title,
                url,
                yt_id,
                spfy_id,
                thumbnail,
                is_aca,
                arng_url,
                categories,
                main_category,
                singable
                ):
    s = models.Song(og_artist=og_artist,
                    aca_artist=aca_artist,
                    title=title,
                    url=url,
                    yt_id=yt_id,
                    spfy_id=spfy_id,
                    thumbnail=thumbnail,
                    is_aca=is_aca,
                    arng_url=arng_url,
                    categories=categories,
                    main_category=main_category,
                    singable=singable)

    db.add(s)
    db.commit()


def create_or_update_vote(db, song_id, user_id, vote):
    vote_entry = db.query(models.Vote).filter(
        (models.Vote.user_id == user_id) & (models.Vote.song_id == song_id)).first()
    if vote_entry:
        vote_entry.vote = str(vote)  # type: ignore
    else:
        vote_entry = models.Vote(song_id=song_id, user_id=user_id, vote=vote)
        db.add(vote_entry)
    db.commit()
