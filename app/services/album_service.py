from app.data import session_factory
from app.data.models.album import Album
from app.config import config


def get_total_music_albums():
    session = session_factory.create_session()
    return session.query(Album).count() or 0


def get_music_albums(all_albums=False, name=None, artist=None, album=None, album_artist=None,
                     composer=None, genre=None,
                     limit=None, start_date=None, end_date=None,
                     album_match_method=None, order_by=None):
    session = session_factory.create_session()
    # noinspection PyComparisonWithNone
    if all_albums:
        albums = session.query(Album).filter(Album.id > 0).all()
        return albums if albums else []

    albums = session.query(Album)
    if album_match_method == 'album_contains':
        albums = albums.filter(Album.name.contains(name))
    elif album_match_method == 'album_starts_with':
        albums = albums.filter(Album.name.startswith(name))
    elif album_match_method == 'album_exact_match':
        albums = albums.filter(Album.name == name)

    if artist:
        albums = albums.filter(Album.artist_tracks.contains(artist))

    if album_artist:
        albums = albums.filter(Album.artist.contains(album_artist))

    if composer:
        albums = albums.filter(Album.composer.contains(composer))

    if genre and genre != 'All':
        albums = albums.filter(Album.genre_internal.contains(
            f'{config.GENRE_WRAPPER}{genre}{config.GENRE_WRAPPER}'))

    if start_date and start_date[:4].isnumeric():
        albums = albums.filter(Album.year >= int(start_date[:4]))

    if end_date and end_date[:4].isnumeric():
        albums = albums.filter(Album.year <= int(end_date[:4]))

    if order_by == 'albumName':
        albums = albums.order_by(Album.name)
    elif order_by == 'artist,albumName':
        albums = albums.order_by(Album.artist, Album.name)
    elif order_by == 'duration,albumName':
        albums = albums.order_by(Album.duration.desc(), Album.name)
    elif order_by == 'year,albumName':
        albums = albums.order_by(Album.year, Album.name)

    if limit:
        albums = albums.limit(limit)

    albums = albums.all()
    return albums if albums else []
