import io
from datetime import datetime

from flask import render_template, send_file, request
import xlsxwriter

from app import app
from app.config.config import (
    EXPORT_FILE_PROPERTIES,
    SONGS_EXPORT_FIELD_TITLES,
    SONGS_EXPORT_FILE_NAME,
    EXPORT_FILE_MIMETYPE,
    SETTINGS_ID,
    config_settings,
    update_config_settings,
    )
from app.data import session_factory
from app.data.models.settings import Settings
from app.services import song_service
from app.tools.logger.logger import log
from app.tools.utils import setup_db

setup_db.setup_db()
total_songs = song_service.get_total_music_songs()


@app.route('/settings', methods=['GET'])
def settings_view():
    return render_template('settings.html',
                           data=config_settings['settings'])


@app.route('/settings_save_changes', methods=['POST'])
def settings_save_changes():
    is_get_spotify_data = 'is_get_spotify_data_flag' in request.form.getlist('flags')
    session = session_factory.create_session()
    settings = session.get(Settings, SETTINGS_ID)
    if settings:
        settings.is_get_spotify_data = is_get_spotify_data
        session.commit()
        update_config_settings(session, Settings)

    return render_template('settings.html',
                           data=config_settings['settings'])


def _get_songs_export_field_values(song, text_left__format, date_format):
    return [
        {'val': song.id, 'format': None},
        {'val': song.album.artist, 'format': text_left__format},
        {'val': song.album.name, 'format': text_left__format},
        {'val': song.disc_number, 'format': None},
        {'val': song.track_number, 'format': None},
        {'val': song.name, 'format': text_left__format},
        {'val': song.duration_rep, 'format': text_left__format},
        {'val': song.year, 'format': text_left__format},
        {'val': song.genre, 'format': text_left__format},
        {'val': song.duration, 'format': text_left__format},
        {'val': song.artist, 'format': text_left__format},
        {'val': song.plays, 'format': None},
        {'val': song.composer, 'format': text_left__format},
        {'val': song.track_id, 'format': None},
        {'val': song.persistent_id, 'format': text_left__format},
        {'val': song.x_id, 'format': text_left__format},
        {'val': song.album.id, 'format': None},
        {'val': song.grouping, 'format': text_left__format},
        {'val': song.work, 'format': text_left__format},
        {'val': song.location, 'format': text_left__format},
        {'val': song.date_released, 'format': date_format},
        {'val': song.date_modified, 'format': date_format},
        {'val': song.date_added, 'format': date_format},
        {'val': song.date_added_orig, 'format': date_format},
        {'val': song.is_data_added_fixed, 'format': None},
        {'val': song.date_imported, 'format': date_format},
        {'val': song.mov_number, 'format': None},
        {'val': song.mov_count, 'format': None},
        {'val': song.mov_name, 'format': None},
        {'val': song.size, 'format': None},
        {'val': song.disc_count, 'format': None},
        {'val': song.track_count, 'format': None},
        {'val': song.bit_rate, 'format': None},
        {'val': song.sample_rate, 'format': None},
        {'val': song.comments, 'format': text_left__format},
        {'val': song.file_folder_count, 'format': None},
        {'val': song.sort_album, 'format': text_left__format},
        {'val': song.sort_artist, 'format': text_left__format},
        {'val': song.sort_composer, 'format': text_left__format},
        {'val': song.sort_name, 'format': text_left__format},
        {'val': song.artwork_count, 'format': None},
        {'val': song.normalization, 'format': None},
        {'val': song.is_user_added, 'format': None},
    ]


def _export_songs_report():
    log.info("Start exporting songs report")
    songs = song_service.get_music_songs_to_export()
    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    workbook.remove_timezone = True

    workbook_properties = EXPORT_FILE_PROPERTIES.copy()
    workbook_properties['created'] = datetime.now()
    workbook.set_properties(workbook_properties)

    worksheet = workbook.add_worksheet('Songs')

    for col, field_titles in enumerate(SONGS_EXPORT_FIELD_TITLES):
        worksheet.set_column(col, col, field_titles.width)

    date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})
    title_format = workbook.add_format({'bg_color': '#BEDFFA'})
    text_left__format = workbook.add_format({'align': 'left'})

    row = 0
    for col, field_titles in enumerate(SONGS_EXPORT_FIELD_TITLES):
        worksheet.write(row, col, field_titles.name, title_format)

    row = 1
    for song in songs:
        col_fields = _get_songs_export_field_values(song, text_left__format, date_format)
        for col, col_field in enumerate(col_fields):
            worksheet.write(row, col, col_field['val'], col_field['format'])
        row += 1

    workbook.close()
    buffer.seek(0)
    log.info("Exporting songs report: Report ready to send.")

    return send_file(buffer, as_attachment=True,
                     download_name=SONGS_EXPORT_FILE_NAME,
                     mimetype=EXPORT_FILE_MIMETYPE)


@app.route('/export_songs_report', methods=['GET'])
def export_songs_report():
    res, error_msg = None, None
    is_error = False
    try:
        res = _export_songs_report()
    except Exception as e:
        is_error = True
        error_msg = "Error exporting songs data"
        log.error("%s. Error msg: %s", error_msg, e)

    return res or render_template('settings.html',
                                  is_error=is_error,
                                  error_msg=error_msg)
