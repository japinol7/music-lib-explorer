from functools import lru_cache
import os
from pathlib import Path

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from app.config.config import config_settings
from app.tools.logger.logger import log
from app.tools.utils import utils
from app.services.song_service import (
    ALBUM_NAME_VARIANTS_TEXT_TO_REMOVE,
    ARTIST_NAME_EXTERNAL_MAPPING,
    ALBUM_NAME_VARIANT_EXTERNAL_MAPPING,
    )
from app.addons.spotify.models.spotify_album import SpotifyAlbum
from app.addons.spotify.models.spotify_artist import SpotifyArtist

MIN_ARTIST_FOLLOWERS = 2
MIN_ARTIST_POPULARITY = 1
ARTISTS_LIMIT_MARGIN_DISCARDED = 25

SPOTIFY_API_LRU_CACHE_SIZE = 32
SPOTIFY_API_KEY_FOLDER = os.path.join(str(Path.home()), '.api_keys', 'spotify_api_keys')
SPOTIFY_API_KEY_FILE = os.path.join(SPOTIFY_API_KEY_FOLDER, 'spotify_client_id.key')
SPOTIFY_API_PRIVATE_KEY_FILE = os.path.join(SPOTIFY_API_KEY_FOLDER, 'spotify_client_secret.key')
os.environ['SPOTIPY_CLIENT_ID'] = utils.read_file_as_string(SPOTIFY_API_KEY_FILE)
os.environ['SPOTIPY_CLIENT_SECRET'] = utils.read_file_as_string(SPOTIFY_API_PRIVATE_KEY_FILE)
SPOTIFY_LOG_PREFIX = 'Spotify. '


class SpotifyController:

    def __init__(self, artist_name, limit, start_date, end_date, artist_match_method,
                 artist_uri_id, order_by, only_artists=False, album_name=None):
        self.artist_name = artist_name
        self.limit = limit
        self.start_date = start_date
        self.end_date = end_date
        self.artist_match_method = artist_match_method
        self.artist_uri_id = artist_uri_id
        self.order_by = order_by
        self.only_artists = only_artists
        self.album_name = album_name
        self.spotify = None

        self.items_len = 0
        self.albums = None
        self.artists = None
        self.error_msg = ''
        self.errors = {'error': self.error_msg}

        self._reset()
        self.soft_reset()

    def _reset(self):
        try:
            self.spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
            self.spotify.search(q='a', type='artist', limit=1)
        except Exception as e:
            log.warning(f"SpotifyException: {e}")
            self.spotify = None
            return
        SpotifyArtist.reset()
        SpotifyAlbum.reset()

    def soft_reset(self):
        SpotifyArtist.reset()
        SpotifyAlbum.reset()

        self.items_len = 0
        self.albums = SpotifyAlbum.albums
        self.artists = SpotifyArtist.artists
        self.error_msg = ''
        self.errors = {'error': self.error_msg}

    def get_spotify_music(self):
        artist_items = []
        artist_results = {}
        album_results = {}
        artist = None

        if not self.spotify:
            self.error_msg = "Cannot initialize Spotify client. Probably the credential keys are not correct."
            log.warning(self.error_msg)
            return

        if not self.artist_name and not self.artist_uri_id and not self.album_name:
            self.error_msg = "Not enough input data."
            res = self._get_response()
            log.info(res)
            return res

        try:
            if self.artist_uri_id:
                artist_data = self.spotify.artist(self.artist_uri_id)
                artist_results = {'artists': {
                    'items': [artist_data],
                    'next': None,
                }}
                artist_items = artist_results['artists']['items']
            elif not self.album_name:
                query = f'artist:{self.artist_name}'
                artist_results = self.spotify.search(q=query, type='artist')
                artist_items = artist_results['artists']['items']
            else:
                query = f'album:{self.album_name}, artist:{self.artist_name}' if self.artist_name else f'album:{self.album_name}'
                album_results = self.spotify.search(q=query, type='album')
                album_results = album_results['albums']
        except spotipy.SpotifyException as e:
            log.warning(f"SpotifyException: {e}")

        if not self.album_name and len(artist_items) < 1:
            self.error_msg = "No artist found" if self.only_artists else "Artist not found"
            res = self._get_response()
            log.info(res)
            return res

        if not self.album_name and len(artist_items) > 1:
            log.warning(f"Found {len(artist_items)} artists that match the artist name: '{self.artist_name}'. "
                        f"We choose the first and discard the rest.")

        if not self.album_name:
            artist_data = artist_items[0]
            artist = SpotifyArtist(artist_data['id'])
            self._fill_artist_fields(artist, artist_data)
            log.info(f"{SPOTIFY_LOG_PREFIX}Artist: {artist.name}, followers: {artist.followers} "
                     f"popularity: {artist.popularity} uri/url {artist.uri} {artist.url}")

        if self.album_name:
            self._get_spotify_albums(album_results)
            self.items_len = len(self.albums)
        elif self.only_artists:
            self._get_spotify_other_artists(artist_results)
            self.items_len = len(SpotifyArtist.artists)
        else:
            self._get_spotify_albums_from_artist(artist)
            self.items_len = len(self.albums)

        return self._get_response()

    def _get_response(self):
        return (
            (self.artist_name, self.limit, self.start_date, self.end_date, self.artist_match_method,
             self.artist_uri_id, self.order_by, self.album_name
             ),
            self.items_len, self.artists, self.albums, self.errors)

    def _get_spotify_albums(self, albums_results):
        albums_data = albums_results['items']
        while albums_results['next'] and len(albums_data) < self.limit:
            albums_results = self.spotify.next(albums_results)['albums']
            albums_data.extend(albums_results['items'])

        for album_data in albums_data[:self.limit]:
            log.info(f"{SPOTIFY_LOG_PREFIX}Album: {album_data['name']}")
            album = SpotifyAlbum(id=album_data['id'])
            artist_data = album_data['artists'][0]
            artist = SpotifyArtist(artist_data['id'])
            artist.name = artist_data['name']
            artist.uri = artist_data['uri']
            artist.url = artist_data['external_urls']['spotify']
            self._fill_album_fields(album, album_data, artist)

    def _get_spotify_albums_from_artist(self, artist):
        albums = []
        albums_results = self.spotify.artist_albums(artist.uri, album_type='album')
        albums_data = albums_results['items']
        while albums_results['next'] and len(albums_data) < self.limit:
            albums_results = self.spotify.next(albums_results)
            albums_data.extend(albums_results['items'])

        for album_data in albums_data[:self.limit]:
            log.info(f"{SPOTIFY_LOG_PREFIX}Album: {album_data['name']}")
            album = SpotifyAlbum(id=album_data['id'])
            self._fill_album_fields(album, album_data, artist)
            albums.append(album)

    def _get_spotify_other_artists(self, artist_results):
        artists_data = artist_results['artists']['items']
        limit_effective = self.limit + ARTISTS_LIMIT_MARGIN_DISCARDED
        while artist_results['artists']['next'] and len(artists_data) < limit_effective:
            artist_results = self.spotify.next(artist_results['artists'])
            artists_data.extend(artist_results['artists']['items'])

        log.info(f"{'-' * 15}")
        for other_artist_data in artists_data[1:]:
            followers = other_artist_data['followers']['total']
            popularity = other_artist_data['popularity']
            if followers < MIN_ARTIST_FOLLOWERS and popularity < MIN_ARTIST_POPULARITY:
                continue
            if len(SpotifyArtist.artists) >= self.limit:
                break
            other_artist = SpotifyArtist(other_artist_data['id'])
            self._fill_artist_fields(other_artist, other_artist_data)
            log.info(f"--- {SPOTIFY_LOG_PREFIX}Another artist: {other_artist.name}, followers: {other_artist.followers} "
                     f"popularity: {other_artist.popularity} uri/url {other_artist.uri} {other_artist.url}")

    def _fill_album_fields(self, album, item, artist):
        album.name = item['name']
        album.artist = artist
        album.artists = [x['name'] for x in item['artists']]
        album.uri = item['uri']
        album.url = item['external_urls']['spotify']
        album.image_url = item['images'] and item['images'][0]['url'] or None
        album.release_date = item['release_date']
        album.total_tracks = item['total_tracks']
        album.album_type = item['album_type']
        album.type = item['type']

    def _fill_artist_fields(self, artist, item):
        artist.name = item['name']
        artist.followers = item['followers']['total']
        artist.uri = item['uri']
        artist.url = item['external_urls']['spotify']
        artist.image_url = item['images'] and item['images'][0]['url'] or None
        artist.popularity = item['popularity']

    @staticmethod
    def get_controller():
        return SpotifyController(
            artist_name=None, limit=1, start_date=None, end_date=None, artist_match_method=None,
            artist_uri_id=None, order_by=None, only_artists=False, album_name=None)


def _get_album_url_from_spotify_music_data(music_data):
    return music_data[3][0].url if music_data[3] else ''


def _spotify_search_variant(music_controller, song, album_artist, album_name, text_to_remove_variant):
    if song.spotify_album_url:
        return

    if text_to_remove_variant not in album_name:
        return

    album_name = album_name.replace(text_to_remove_variant, '').strip()
    log.info(f"{SPOTIFY_LOG_PREFIX}Search album name variant: {album_name} | artist_name: {album_artist}")
    sp_music_data = _get_spotify_data(music_controller, album_artist, album_name)
    song.spotify_album_url = _get_album_url_from_spotify_music_data(sp_music_data)


@lru_cache(maxsize=SPOTIFY_API_LRU_CACHE_SIZE)
def _get_spotify_data(controller, album_artist, album_name):
    controller.soft_reset()
    controller.album_name = album_name
    controller.artist_name = album_artist
    return controller.get_spotify_music()


def get_spotify_data(song):
    album_artist = song.album.artist.lower()
    album_artist = ARTIST_NAME_EXTERNAL_MAPPING.get(album_artist, album_artist)

    song_album_name = song.album.name.lower()
    for orig_subtext, new_subtext in ALBUM_NAME_VARIANT_EXTERNAL_MAPPING.items():
        song_album_name = song_album_name.replace(orig_subtext, new_subtext)

    log.info(f"{SPOTIFY_LOG_PREFIX}Search album with name ..: {song_album_name} | artist_name: {album_artist}")

    if not config_settings['spotify_controller']:
        config_settings['spotify_controller'] = SpotifyController.get_controller()
    music_controller = config_settings['spotify_controller']

    sp_music_data = _get_spotify_data(music_controller, album_artist, song_album_name)
    song.spotify_album_url = _get_album_url_from_spotify_music_data(sp_music_data)

    for text_to_remove_variant in ALBUM_NAME_VARIANTS_TEXT_TO_REMOVE:
        _spotify_search_variant(music_controller, song, album_artist, song_album_name, text_to_remove_variant)
