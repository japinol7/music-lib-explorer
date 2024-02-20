from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import false, true

from app.data import session_factory
from app.data.models.song import Song
from app.data.models.album import Album

ALBUM_NAME_VARIANTS_TEXT_TO_REMOVE = [
    "(remastered)",
    "[remastered]",
    "remastered",
    "remaster",
    "(bonus version)",
    "[bonus version]",
    "bonus version",
    "(exclusive bonus track version)",
    "[exclusive bonus track version]",
    "exclusive bonus track version",
    "(bonus track version)",
    "[bonus track version]",
    "bonus track version",
    "deluxe version",
    "35th anniversary edition (remastered)",
    "30th anniversary edition (remastered)",
    "25th anniversary edition (remastered)",
    "35th anniversary remaster",
    "30th anniversary remaster",
    "25th anniversary remaster",
    "35th anniversary edition",
    "30th anniversary edition",
    "25th anniversary edition",
    "(35th anniversary 2019 remastered)",
    "35th anniversary 2019 remastered",
    "35th anniversary best perfect edition special edition",
    "35th anniversary best perfect edition",
    "40th anniversary edition",
    "50th anniversary edition",
    "anniversary edition (remastered)",
    "anniversary edition",
    "remastered edition",
    "[original motion picture soundtrack]",
    "(original motion picture soundtrack)",
    "original motion picture soundtrack",
    "original jazz classics remasters",
    "soundtrack from the motion picture",
    "original motion picture",
    "(original soundtrack)",
    "original soundtrack",
    "soundtrack",
    "special edition",
    "deluxe edition",
    "(platinum edition)",
    "platinum edition",
    ]


ALBUM_NAME_VARIANT_EXTERNAL_MAPPING = {
    'anzenchitai': 'anzen chitai',
    }

ARTIST_NAME_EXTERNAL_MAPPING = {
    'anzenchitai': 'anzen chitai',
    }


def get_total_music_songs():
    session = session_factory.create_session()
    return session.query(Song).count() or 0


def get_music_songs(all_songs=False, name=None, artist=None, album=None, album_artist=None,
                    composer=None, genre=None,
                    limit=None, start_date=None, end_date=None,
                    song_match_method=None, song_user_added=None, order_by=None):

    # noinspection PyComparisonWithNone
    session = session_factory.create_session()

    songs = session.query(Song)
    # Use joined loading instead of lazy loading to prevent DetachedInstanceError error when reloading page
    songs = songs.options(joinedload(Song.album))
    songs = songs.join(Song.album)

    if all_songs:
        songs.filter(Song.id > 0).all()
        return songs if songs else []

    if song_match_method == 'song_contains':
        songs = songs.filter(Song.name.contains(name))
    elif song_match_method == 'song_starts_with':
        songs = songs.filter(Song.name.startswith(name))
    elif song_match_method == 'song_exact_match':
        songs = songs.filter(Song.name == name)

    if song_user_added == 'Added by user':
        songs = songs.filter(Song.is_user_added == true())
    elif song_user_added == 'Automatically added':
        songs = songs.filter(Song.is_user_added == false())

    if artist:
        songs = songs.filter(Song.artist.contains(artist))

    if album:
        songs = songs.filter(Album.name.contains(album))

    if album_artist:
        songs = songs.filter(Album.artist.contains(album_artist))

    if composer:
        songs = songs.filter(Song.composer.contains(composer))

    if genre and genre != 'All':
        songs = songs.filter(Song.genre.like(genre))

    if start_date and start_date[:4].isnumeric():
        songs = songs.filter(Song.year >= int(start_date[:4]))

    if end_date and end_date[:4].isnumeric():
        songs = songs.filter(Song.year <= int(end_date[:4]))

    if order_by == 'songName':
        songs = songs.order_by(Song.name)
    elif order_by == 'artist,album,disc,track':
        songs = songs.order_by(Album.artist, Album.name, Song.disc_number, Song.track_number)
    elif order_by == 'album,disc,track':
        songs = songs.order_by(Album.name, Song.disc_number, Song.track_number)
    elif order_by == 'album,songName':
        songs = songs.order_by(Album.name, Song.name)
    elif order_by == 'artist,album,songName':
        songs = songs.order_by(Album.artist, Album.name, Song.name)
    elif order_by == 'artist,songName':
        songs = songs.order_by(Album.artist, Song.name)
    elif order_by == 'plays,songName':
        songs = songs.order_by(Song.plays.desc(), Song.name)
    elif order_by == 'duration,songName':
        songs = songs.order_by(Song.duration.desc(), Song.name)
    elif order_by == 'year,songName':
        songs = songs.order_by(Song.year, Song.name)

    if limit:
        songs = songs.limit(limit)

    songs = songs.all()
    return songs if songs else []


def get_music_songs_to_export():
    songs = get_music_songs(all_songs=True)
    songs = songs.order_by(Album.artist, Album.name, Song.disc_number, Song.track_number)
    return songs if songs else []
