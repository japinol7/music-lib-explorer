from pathlib import Path
from urllib.parse import unquote, urlparse
import webbrowser

from flask import render_template, request, redirect
from app import app
from app.data import session_factory

from app.config.config import config_settings
from app.tools.logger.logger import log
from app.data.models.song import Song
from app.services import data_service, song_service
from app.tools.utils import setup_db, import_data
from app.addons.spotify.controller.spotify_controller import get_spotify_data

setup_db.setup_db()
total_songs = song_service.get_total_music_songs()


@app.route('/music-lib-songs', methods=['GET', 'POST'])
def music_lib_songs():
    global total_songs
    songs = []
    form_executed = None
    if request.method == 'POST' and 'music_song_title' in request.form:
        name = request.form.get('music_song_title')
        artist = request.form.get('music_artist_name')
        album_artist = request.form.get('music_album_artist')
        album = request.form.get('music_album_name')
        composer = request.form.get('music_composer')
        genre = request.form.get('music_genre')
        limit = request.form.get('music_song_limit')
        start_date = request.form.get('music_song_start_date')
        end_date = request.form.get('music_song_end_date') or start_date
        song_match_method = request.form.get('music_song_title_method')
        song_user_added = request.form.get('music_song_user_added')
        order_by = request.form.get('music_song_order_by')
        songs = get_music_songs(name, artist, album, album_artist, composer, genre, limit,
                                start_date, end_date, song_match_method, song_user_added, order_by)
        form_executed = 'music_lib_form'
    elif request.method == 'POST' and 'import_data_method' in request.form:
        import_data.import_if_empty()
        error = f"Data already imported. Songs in the database: {total_songs or song_service.get_total_music_songs()}."
        songs_res = []
        songs = (('', ''), len(songs_res), {}, songs_res, {'error': error})
        form_executed = 'music_lib_import_data_form'
    elif request.method == 'POST' and 'music_song_location' in request.form:
        song_uri = request.form.get('music_song_location')
        file_path = unquote(urlparse(song_uri).path)[1:]
        file_path_obj = Path(file_path)
        if file_path_obj.is_file():
            webbrowser.open(file_path)
        form_executed = 'music_song_play_form'
    return render_template('music_lib_songs.html',
                           songs=songs,
                           settings=config_settings['settings'],
                           form_executed=form_executed)


def get_music_songs(name, artist, album, album_artist, composer, genre, limit,
                    start_date, end_date, song_match_method, song_user_added, order_by):
    error = ''
    songs = []
    if data_service.is_music_lib_imported():
        songs = song_service.get_music_songs(all_songs=False, name=name, artist=artist, album=album,
                                             album_artist=album_artist, composer=composer, genre=genre,
                                             limit=limit, start_date=start_date, end_date=end_date,
                                             song_match_method=song_match_method, song_user_added=song_user_added,
                                             order_by=order_by)
    else:
        error = 'There is no data on the database. Please, import some data.'

    music_gen_data = {}
    return ((name, limit, start_date, end_date, song_match_method, order_by,
             artist, album, total_songs or song_service.get_total_music_songs(),
             composer, genre, album_artist, song_user_added),
            len(songs), music_gen_data, songs, {'error': error})


@app.route('/spotify-lib-song', methods=['POST'])
def spotify_lib_song():
    if request.method == 'POST' and 'spotify_album_from_song' in request.form:
        song_id = request.form.get('spotify_album_from_song')

        if not song_id or not song_id.isnumeric():
            log.warning(f"Invalid song id: {song_id}")
            return redirect('/music-lib-songs')

        session = session_factory.create_session()
        song = session.get(Song, song_id)

        if not song or not song.id:
            log.warning(f"Invalid song id: {song_id}")
            return redirect('/music-lib-songs')

        get_spotify_data(song)

        if not song.spotify_album_url:
            log.warning("No Spotify album found for album: %s and artist: %s", song.album.name, song.album.artist)
            return redirect('/music-lib-songs')

        return redirect(song.spotify_album_url)
