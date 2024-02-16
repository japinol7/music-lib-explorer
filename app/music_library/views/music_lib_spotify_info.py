from flask import render_template, request, redirect
from app import app
from app.data import session_factory

from app.config.config import config_settings
from app.tools.logger.logger import log
from app.data.models.album import Album
from app.services import album_service, data_service
from app.tools.utils import setup_db
from app.addons.spotify.controller.spotify_controller import get_spotify_data_album, get_spotify_data_artist

setup_db.setup_db()
total_albums = album_service.get_total_music_albums()


def _music_lib_spotify_info_render_template(artist=None, album=None, artist_albums=None):
    return render_template(
        'music_lib_spotify_info.html',
        artist=artist,
        album=album,
        artist_albums=artist_albums or [],
        settings=config_settings['settings'],
        spotify_client_init=config_settings['spotify_controller']
                            and config_settings['spotify_controller'].spotify and True or False)


@app.route('/spotify-lib-album-info', methods=['GET', 'POST'])
def music_lib_spotify_info():
    album_id = request.form.get('spotify_info_from_album')

    if not album_id or not album_id.isnumeric():
        log.warning(f"Invalid album id: {album_id}")
        return _music_lib_spotify_info_render_template()

    session = session_factory.create_session()
    album = session.get(Album, album_id)

    if not album or not album.id or len(album.songs) < 1:
        log.warning(f"Invalid album id: {album_id}")
        return _music_lib_spotify_info_render_template()

    first_song = album.songs[0]

    sp_music_data = get_spotify_data_artist(first_song)

    if not sp_music_data or not sp_music_data[2] or len(sp_music_data[2]) < 1:
        log.warning("No Spotify artist found for artist: %s", album.artist)
        return _music_lib_spotify_info_render_template()

    artist = sp_music_data[2][0]

    sp_music_data = get_spotify_data_album(first_song)

    if not sp_music_data or not sp_music_data[3] or len(sp_music_data[3]) < 1:
        log.warning("No Spotify album found for artist: %s", album.artist)
        return _music_lib_spotify_info_render_template(artist=artist)

    album = sp_music_data[3][0]

    return _music_lib_spotify_info_render_template(artist=artist, album=album)
