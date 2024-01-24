from collections import Counter
import logging
from zipfile import ZipFile

from app.data import session_factory
from app.data.models.song import Song
from app.data.models.album import Album
from app.data.models.user import User
from app.services import  user_service
from app.data.dataset.csv_dataset import CsvDataset
from app.data.dataset.xml_dataset import XmlDataset
from app.config import config
from app.config.config import DATASET_SOURCE_FORMAT as FORMAT
from app.config.config import ALLOW_TO_IMPORT_SEVERAL_FILES
from app.utils.utils import time_seconds_format_to_hms, time_seconds_format_to_min_sec

logging.basicConfig(format=config.LOGGER_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ImportDataException(Exception):
    pass


def import_if_empty():
    __unzip_data_files()
    __import_music_songs()
    __import_users()


def __unzip_data_files():
    session = session_factory.create_session()
    if session.query(Song).count() > 0:
        return

    logger.info("Unzip database files")
    try:
        with ZipFile(config.DATASET_FILE_ZIP) as fin_zip:
            fin_zip.extractall(config.RESOURCES_FOLDER)
    except FileNotFoundError:
        raise ImportDataException(f"Error extracting database files. File not found: {config.DATASET_FILE_ZIP}")
    except Exception as e:
        raise ImportDataException(f"Error extracting database files from: {config.DATASET_FILE_ZIP}. Error msg: {e}")


def __get_dataset_from_csv():
    with open(config.DATASET_FILE, 'r', encoding='utf8') as fin:
        data = fin.read()
    return CsvDataset(data).get_grouped(config.COLUMN_TO_GROUP_BY)


def __get_dataset_from_json():
    with open(config.DATASET_FILE, 'r', encoding='utf8') as fin:
        data = fin.read()
    return CsvDataset(data).get_grouped(config.COLUMN_TO_GROUP_BY)


def __get_dataset_from_xml():
    with open(config.DATASET_FILE, 'r', encoding='utf8') as fin:
        data = fin.read()
    return XmlDataset(data).get_grouped(config.COLUMN_TO_GROUP_BY)


def __import_music_songs():
    session = session_factory.create_session()
    if not ALLOW_TO_IMPORT_SEVERAL_FILES and session.query(Song).count() > 0:
        return

    logger.info("Start to Import music lib songs file")
    if config.DATASET_SOURCE_FORMAT == config.DATASET_SOURCE_CSV:
        dataset = __get_dataset_from_csv()
    elif config.DATASET_SOURCE_FORMAT == config.DATASET_SOURCE_XML:
        dataset = __get_dataset_from_xml()
    elif config.DATASET_SOURCE_FORMAT == config.DATASET_SOURCE_JSON:
        dataset = __get_dataset_from_json()
    else:
        raise ImportDataException(f"Internal Error extracting database files. "
                                  f"Source Format not supported: {config.DATASET_SOURCE_FORMAT}")

    count_albums = 0
    count_songs = 0
    for key, rows in dataset:
        if not key:
            continue
        count_albums += 1
        rows_list = list(rows)
        album = Album()
        album.name = rows_list[0]['album']
        album.artist = rows_list[0]['album_artist'] if rows_list[0]['album_artist'] else None
        album.disc_count_total = int(rows_list[0]['disc_count']) if rows_list[0]['disc_count'] else 0
        album.track_count_total = int(rows_list[0]['track_count']) if rows_list[0]['track_count'] else 0
        track_count_total = Counter()
        album.year_max = max([x['year'] for x in rows_list])
        album.year_min = min([x['year'] for x in rows_list])
        album.year = album.year_min
        artist_tracks = set()
        genre = set()
        genre_internal = set()
        composer = set()
        album_track_count = 0
        album.duration = 0
        for row in rows_list:
            if not row['track_count'] or not row['sample_rate']:
                # If some required columns are missing, it is probably not an audio song. It may be a video
                continue
            count_songs += 1
            album_track_count += 1
            song = Song()
            song.name = row['name']
            song.album = album
            song.artist = row['artist']
            song.disc_number = int(row['disc_number']) if row['disc_number'] else 0
            song.disc_count = int(row['disc_count']) if row['disc_count'] else 0
            song.track_number = int(row['track_number']) if row['track_number'] else 0
            song.track_count = int(row['track_count']) if row['track_count'] else 0
            track_count_total[song.disc_number] = song.track_count
            song.duration = row['time'] and int(row['time']) or 0
            song.duration = song.duration if FORMAT != 'xml' else song.duration // 1000
            song.duration_rep = time_seconds_format_to_min_sec(song.duration)
            song.size = row['size']
            song.year = row['year']
            song.composer = row['composer']
            song.genre = row['genre']
            song.grouping = row['grouping']
            song.work = row['work']
            song.mov_number = row['mov_number']
            song.mov_count = row['mov_count']
            song.mov_name = row['mov_name']
            song.plays = row['plays'] and int(row['plays']) or 0
            song.date_released = row['date_released']
            song.date_modified = row['date_modified']
            song.date_added = row['date_added']
            if config.DATASET_SOURCE_FORMAT == config.DATASET_SOURCE_XML:
                # Fix date added field only if we are reading the xml version of the dataset
                song.date_added_orig = row['date_added']
                if song.date_added and song.date_released and song.date_added < song.date_released:
                    song.date_added = song.date_released
                    song.is_data_added_fixed = True
                # Add some plays so the each song, without losing their order value, just the distance between them
                song.plays = song.plays + config.PLAYS_TO_ADD_ALL_SONGS
                song.is_user_added = config.IS_USER_ADDED
            else:
                song.is_user_added = int(row['is_user_added']) and True or False
            song.bit_rate = row['bit_rate']
            song.sample_rate = row['sample_rate']
            song.comments = row['comments']
            if row['location'] and config.FILE_LOCATION_REPLACE.old:
                song.location = row['location'].replace(
                    config.FILE_LOCATION_REPLACE.old,
                    config.FILE_LOCATION_REPLACE.new)
            else:
                song.location = row['location']
            song.persistent_id = row['persistent_id'] if row['persistent_id'] else None
            song.track_id = row['track_id']
            song.file_folder_count = row['file_folder_count']
            song.sort_album = row['sort_album']
            song.sort_artist = row['sort_artist']
            song.sort_name = row['sort_name']
            song.artwork_count = row['artwork_count']
            song.x_id = config.DELIMITER.join([
                row['persistent_id'] or '',
                f"{song.duration and int(song.duration) or 0:05d}",
                ])
            session.add(song)
            if song.artist:
                artist_tracks.add(song.artist)
            if song.genre:
                genre.add(song.genre)
                genre_internal.add(f'{config.GENRE_WRAPPER}{song.genre}{config.GENRE_WRAPPER}')
            if song.composer:
                composer.add(song.composer)
            album.duration += song.duration
            album.track_count = album_track_count

        album.artist_tracks = config.DELIMITER.join(list(artist_tracks))
        album.tracks_on_discs = str(dict(sorted(track_count_total.items())))
        album.track_count_total = sum(track_count_total.values())
        album.genre = ', '.join(list(genre))
        album.genre_internal = ', '.join(list(genre_internal))
        album.composer = config.DELIMITER.join(list(composer))
        if album.duration // 3600 > 0:
            album.duration_rep = time_seconds_format_to_hms(album.duration)
        else:
            album.duration_rep = time_seconds_format_to_min_sec(album.duration)

        album.x_id = config.DELIMITER.join([
            album.artist,
            album.name,
            ])
        logger.info(f"Adding album num {count_albums:6} to database: {key}")
        session.add(album)

    logger.info("Committing to database")
    session.commit()
    logger.info("End Import music lib songs file")


def __import_users():
    session = session_factory.create_session()
    if session.query(User).count() > 0:
        return

    user_service.get_default_user()

    user2 = User()
    user2.email = 'test_user_2@test.test.com.test'
    user2.name = 'User 2'
    session.add(user2)
    session.commit()
