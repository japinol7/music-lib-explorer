from flask import render_template, request, redirect
from app import app
from app.data import session_factory

from app.config.config import config_settings
from app.tools.logger.logger import log
from app.data.models.album import Album
from app.services import album_service, data_service
from app.tools.utils import setup_db
from app.tools.utils import import_data
from app.addons.spotify.controller.spotify_controller import get_spotify_data_album, get_spotify_data_artist

setup_db.setup_db()
total_albums = album_service.get_total_music_albums()


@app.route('/music-lib-albums', methods=['GET', 'POST'])
def music_lib_albums():
    global total_albums
    albums = []
    form_executed = None
    if request.method == 'POST' and 'music_album_name' in request.form:
        name = request.form.get('music_album_name')
        artist = request.form.get('music_artist_name')
        album_artist = request.form.get('music_album_artist')
        album = request.form.get('music_album_name')
        composer = request.form.get('music_composer')
        genre = request.form.get('music_genre')
        limit = request.form.get('music_album_limit')
        start_date = request.form.get('music_album_start_date')
        end_date = request.form.get('music_album_end_date') or start_date
        album_match_method = request.form.get('music_album_title_method')
        order_by = request.form.get('music_album_order_by')
        albums = get_music_albums(
            name, artist, album, album_artist, composer, genre, limit,
            start_date, end_date, album_match_method, order_by)
        form_executed = 'music_lib_form'
    elif request.method == 'POST' and 'import_data_method' in request.form:
        import_data.import_if_empty()
        error = f"Data already imported. Albums in the database: " \
                f"{total_albums or album_service.get_total_music_albums()}."
        albums_res = []
        albums = (('', ''), len(albums_res), {}, albums_res, {'error': error})
        form_executed = 'music_lib_import_data_form'

    return render_template(
        'music_lib_albums.html',
        albums=albums,
        settings=config_settings['settings'],
        form_executed=form_executed)


def get_music_albums(name, artist, album, album_artist, composer, genre, limit,
                     start_date, end_date, album_match_method, order_by):
    error = ''
    albums = []
    if data_service.is_music_lib_imported():
        albums = album_service.get_music_albums(
            all_albums=False, name=name, artist=artist, album=album,
            album_artist=album_artist, composer=composer, genre=genre,
            limit=limit, start_date=start_date, end_date=end_date,
            album_match_method=album_match_method, order_by=order_by)
    else:
        error = 'There is no data on the database. Please, import some data.'

    music_gen_data = {}
    return ((name, limit, start_date, end_date, album_match_method, order_by,
             artist, album, total_albums or album_service.get_total_music_albums(),
             composer, genre, album_artist),
            len(albums), music_gen_data, albums, {'error': error})


@app.route('/spotify-lib-album', methods=['POST'])
def spotify_lib_album():
    if request.method == 'POST' and 'spotify_album_from_album' in request.form:
        album_id = request.form.get('spotify_album_from_album')

        if not album_id or not album_id.isnumeric():
            log.warning(f"Invalid album id: {album_id}")
            return redirect('/music-lib-albums')

        session = session_factory.create_session()
        album = session.get(Album, album_id)

        if not album or not album.id or len(album.songs) < 1:
            log.warning(f"Invalid album id: {album_id}")
            return redirect('/music-lib-albums')

        first_song = album.songs[0]
        get_spotify_data_album(first_song)

        if not first_song.spotify_album_url:
            log.warning("No Spotify album found for album: %s and artist: %s",
                        album.name, album.artist)
            return redirect('/music-lib-albums')

        return redirect(first_song.spotify_album_url)
    return None


@app.route('/spotify-lib-album-artist', methods=['POST'])
def spotify_lib_album_artist():
    if request.method == 'POST' and 'spotify_album_from_album' in request.form:
        album_id = request.form.get('spotify_album_from_album')

        if not album_id or not album_id.isnumeric():
            log.warning(f"Invalid album id: {album_id}")
            return redirect('/music-lib-albums')

        session = session_factory.create_session()
        album = session.get(Album, album_id)

        if not album or not album.id or len(album.songs) < 1:
            log.warning(f"Invalid album id: {album_id}")
            return redirect('/music-lib-albums')

        first_song = album.songs[0]
        get_spotify_data_artist(first_song)

        if not first_song.spotify_artist_url:
            log.warning("No Spotify album found for artist: %s", album.artist)
            return redirect('/music-lib-albums')

        return redirect(first_song.spotify_artist_url)
    return None
