import os
import pathlib

from collections import namedtuple, OrderedDict

STR_ENCODING = 'utf-8'

SETTINGS_ID = 1
DEFAULT_IS_GET_SPOTIFY_DATA = True

config_settings = {'settings': None}

DATASET_SOURCE_FORMAT = 'csv'

DELIMITER_CSV = ','
DECIMAL_SEPARATOR_CSV = '.'
THOUSANDS_SEPARATOR_CSV = '.' if DECIMAL_SEPARATOR_CSV == ',' else ','

ROOT_FOLDER = pathlib.Path(__file__).parent.parent
RESOURCES_FOLDER = os.path.join(ROOT_FOLDER, 'resources')
DATASET_FOLDER = os.path.join(ROOT_FOLDER, 'resources', 'data')
DATASET_FOLDER_ZIP = os.path.join(DATASET_FOLDER, 'zip')
DATASET_FILE_ZIP = os.path.join(DATASET_FOLDER_ZIP, 'data.zip')

DELIMITER = '.||.'
GENRE_WRAPPER = '||'

DATASET_FILE_NAME = 'music_dig_lib'
DATASET_FILE = os.path.join(DATASET_FOLDER, f'{DATASET_FILE_NAME}.{DATASET_SOURCE_FORMAT}')

DATASET_SOURCE_CSV = 'csv'
DATASET_SOURCE_JSON = 'json'
DATASET_SOURCE_XML = 'xml'
ColumnsMapping = namedtuple('columns_mapping', [DATASET_SOURCE_CSV, DATASET_SOURCE_JSON, DATASET_SOURCE_XML])
COLUMNS_MAPPING = OrderedDict({
    'name': ColumnsMapping('name', 'name', 'Name'),
    'artist': ColumnsMapping('artist', 'artist', 'Artist'),
    'album_artist': ColumnsMapping('album_artist', 'artist', 'Album Artist'),
    'composer': ColumnsMapping('composer', 'composer', 'Composer'),
    'album': ColumnsMapping('album', 'album', 'Album'),
    'grouping': ColumnsMapping('grouping', 'grouping', 'Grouping'),
    'work': ColumnsMapping('work', 'work', 'Work'),
    'mov_number': ColumnsMapping('mov_number', 'movNumber', 'Movement Number'),
    'mov_count': ColumnsMapping('mov_count', 'movCount', 'Movement Count'),
    'mov_name': ColumnsMapping('mov_name', 'mov_name', 'Movement Name'),
    'genre': ColumnsMapping('genre', 'genre', 'Genre'),
    'size': ColumnsMapping('size', 'size', 'Size'),
    'time': ColumnsMapping('duration', 'duration', 'Total Time'),
    'disc_number': ColumnsMapping('disc_number', 'discNumber', 'Disc Number'),
    'disc_count': ColumnsMapping('disc_count', 'discCount', 'Disc Count'),
    'track_id': ColumnsMapping('track_id', 'trackId', 'Track ID'),
    'track_number': ColumnsMapping('track_number', 'trackNumber', 'Track Number'),
    'track_count': ColumnsMapping('track_count', 'trackCount', 'Track Count'),
    'year': ColumnsMapping('year', 'year', 'Year'),
    'date_released': ColumnsMapping('date_released', 'dateReleased', 'Release Date'),
    'date_added': ColumnsMapping('date_added', 'dateAdded', 'Date Added'),
    'date_added_orig': ColumnsMapping('date_added_orig', 'dateAddedOriginal', 'Date Added Original'),
    'is_data_added_fixed': ColumnsMapping('is_data_added_fixed', 'isDateAddedFixed', 'Is Data Added Fixed'),
    'date_modified': ColumnsMapping('date_modified', 'dateModified', 'Date Modified'),
    'bit_rate': ColumnsMapping('bit_rate', 'bitRate', 'Bit Rate'),
    'sample_rate': ColumnsMapping('sample_rate', 'sampleRate', 'Sample Rate'),
    'comments': ColumnsMapping('comments', 'comments', 'Comments'),
    'plays': ColumnsMapping('plays', 'plays', 'Play Count'),
    'location': ColumnsMapping('location', 'location', 'Location'),
    'persistent_id': ColumnsMapping('persistent_id', 'persistentId', 'Persistent ID'),
    'x_id': ColumnsMapping('x_id', 'xId', 'External ID'),
    'file_folder_count': ColumnsMapping('file_folder_count', 'fileFolderCount', 'File Folder Count'),
    'sort_album': ColumnsMapping('sort_album', 'sortAlbum', 'Sort Album'),
    'sort_artist': ColumnsMapping('sort_artist', 'sortArtist', 'Sort Artist'),
    'sort_composer': ColumnsMapping('sort_composer', 'sortComposer', 'Sort Composer'),
    'sort_name': ColumnsMapping('sort_name', 'sortName', 'Sort Name'),
    'artwork_count': ColumnsMapping('artwork_count', 'artworkCount', 'Artwork Count'),
    'normalization': ColumnsMapping('normalization', 'normalization', 'Normalization'),
    'is_user_added': ColumnsMapping('is_user_added', 'isUserAdded', 'Is User Added'),
    })

COLUMNS_XML_KEYS = OrderedDict({item.xml: None for item in COLUMNS_MAPPING.values()})
COLUMNS_XML_MAPPING = {x[0]: x[1] for x in zip(COLUMNS_XML_KEYS, COLUMNS_MAPPING)}
COLUMNS_XML_REQUIRED = ['Album', 'Track Number']

COLUMN_TO_GROUP_BY = 'artist_and_album'

ColumnToAddToGroup = namedtuple('column_to_add_to_group', ['new_column', 'column1', 'column2'])
COLUMN_TO_ADD_TO_GROUP = ColumnToAddToGroup('artist_and_album', 'album_artist', 'album')

DATE_COLUMNS = ['date_released', 'date_added', 'date_modified']
AMOUNT_COLUMNS = []
COLUMNS_TO_STRIP_WHITESPACE_FROM = []

# Adjustments to a particular dataset. Added here for convenience.
# Remember that the xml dataset will be imported only once, just to generate the csv or json datasets
PLAYS_TO_ADD_ALL_SONGS = 0
FileLocationReplace = namedtuple('file_location_replace', ['old', 'new'])
FILE_LOCATION_REPLACE = FileLocationReplace('', '')
ALLOW_TO_IMPORT_SEVERAL_FILES = False
IS_USER_ADDED = False
# End Adjustments to a particular dataset

# Songs export settings
SONGS_EXPORT_FILE_NAME = 'songs_report.xlsx'
SONGS_EXPORT_FIELD_NORMAL_WIDTH = 17
songs_export_field_titles = namedtuple('songs_export_field_titles', ['name', 'width'])
SONGS_EXPORT_FIELD_TITLES = [
    songs_export_field_titles('id', 12),
    songs_export_field_titles('album_artist', 47),
    songs_export_field_titles('album', 67),
    songs_export_field_titles('disc_number', 14),
    songs_export_field_titles('track_number', 14),
    songs_export_field_titles('song_name', 76),
    songs_export_field_titles('duration_rep', 15),
    songs_export_field_titles('year', 9),
    songs_export_field_titles('genre', 26),
    songs_export_field_titles('duration', 13),
    songs_export_field_titles('artist', 59),
    songs_export_field_titles('plays', 19),
    songs_export_field_titles('composer', 69),
    songs_export_field_titles('track_id', 14),
    songs_export_field_titles('persistent_id', 28),
    songs_export_field_titles('x_id', 38),
    songs_export_field_titles('album_id', 18),
    songs_export_field_titles('grouping', 22),
    songs_export_field_titles('work', 50),
    songs_export_field_titles('location', 110),
    songs_export_field_titles('date_released', 16),
    songs_export_field_titles('date_modified', 16),
    songs_export_field_titles('date_added', 16),
    songs_export_field_titles('date_added_orig', 18),
    songs_export_field_titles('is_data_added_fixed', 18),
    songs_export_field_titles('date_imported', 17),
    songs_export_field_titles('mov_number', SONGS_EXPORT_FIELD_NORMAL_WIDTH),
    songs_export_field_titles('mov_count', SONGS_EXPORT_FIELD_NORMAL_WIDTH),
    songs_export_field_titles('mov_name', 42),
    songs_export_field_titles('size', SONGS_EXPORT_FIELD_NORMAL_WIDTH),
    songs_export_field_titles('disc_count', 15),
    songs_export_field_titles('track_count', 15),
    songs_export_field_titles('bit_rate', SONGS_EXPORT_FIELD_NORMAL_WIDTH),
    songs_export_field_titles('sample_rate', SONGS_EXPORT_FIELD_NORMAL_WIDTH),
    songs_export_field_titles('comments', 80),
    songs_export_field_titles('file_folder_count', 15),
    songs_export_field_titles('sort_album', 67),
    songs_export_field_titles('sort_artist', 59),
    songs_export_field_titles('sort_composer', 50),
    songs_export_field_titles('sort_name', 76),
    songs_export_field_titles('artwork_count', SONGS_EXPORT_FIELD_NORMAL_WIDTH),
    songs_export_field_titles('normalization', SONGS_EXPORT_FIELD_NORMAL_WIDTH),
    songs_export_field_titles('is_user_added', SONGS_EXPORT_FIELD_NORMAL_WIDTH),
    ]
EXPORT_FILE_PROPERTIES = {
    'title': 'Song list report from MusicLME',
    'subject': 'Song list report from MusicLME',
    'author': 'Music Library Metadata Explorer - MusicLME',
    'keywords': 'song, MusicLME',
    'comments': 'Created with Music Library Metadata Explorer',
    }
EXPORT_FILE_MIMETYPE = 'application/xlsx'


def update_config_settings(session, settings_model):
    settings = session.get(settings_model, SETTINGS_ID)
    if not settings:
        settings = settings_model()
        settings.id = SETTINGS_ID
        settings.is_get_spotify_data = DEFAULT_IS_GET_SPOTIFY_DATA
        session.add(settings)
        session.commit()

    config_settings['settings'] = settings
    config_settings['spotify_controller'] = None
    return settings
