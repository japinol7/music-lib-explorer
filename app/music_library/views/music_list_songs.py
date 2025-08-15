from flask import render_template, request
from app import app

from app.config.config import config_settings
from app.tools.logger.logger import log
from app.services import music_list_service
from app.tools.utils import setup_db

setup_db.setup_db()
total_mb_songs = music_list_service.get_total_music_list_songs()

@app.route('/music-list-songs', methods=['GET', 'POST'])
def music_list_songs():
    global total_mb_songs
    songs = []
    form_executed = None
    if request.method == 'POST':
        log.info("music_list_songs POST called.")
        form_executed = 'music_list_songs_form'
        songs = music_list_service.get_music_list_songs()
        songs = (songs, len(songs))
    return render_template(
        'music_list_songs.html',
        songs=songs,
        settings=config_settings['settings'],
        form_executed=form_executed)
