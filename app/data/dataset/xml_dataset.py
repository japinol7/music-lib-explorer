from datetime import datetime
from decimal import Decimal
from collections import OrderedDict
import xml.etree.ElementTree as etree

from ...config import config
from ...config.config import COLUMN_TO_ADD_TO_GROUP
from .dataset import Dataset


class XmlDataset(Dataset):
    """Represents an xml a dataset structured as a list of dictionaries.
    This xml dataset is a special version for a specific kind of xml structure
    and will not work for any kind of xml file.
    """

    def __init__(self, dataset):
        super().__init__(dataset)
        self.dataset_source = config.DATASET_SOURCE_XML
        self.logger.debug('Reading an xml dataset')

    def _process(self, dataset):
        """Overrides _process to process the dataset from an xml resource.
        Transforms the given dataset to a list of ordered dictionaries.
        """
        tree = etree.parse(config.DATASET_FILE)
        root = tree.getroot()
        main_dict = root.findall('dict')
        for item in list(main_dict[0]):
            if item.tag == "dict":
                tracks_dict = item
                break
        tracklist = list(tracks_dict.findall('dict'))

        songs = []
        for item in tracklist:
            track = list(item)
            song = {}
            for i in range(len(track)):
                if track[i].text in config.COLUMNS_XML_KEYS:
                    song.update({
                        track[i].text: track[i + 1].text})

            # If some required columns are missing, it is probably not a song
            for key in config.COLUMNS_XML_REQUIRED:
                if not song.get(key):
                    continue
            songs.append(song)

        # Add missing keys
        for song in songs:
            for key in config.COLUMNS_XML_KEYS:
                if not song.get(key):
                    song[key] = ''

        dataset = (OrderedDict(x.items()) for x in songs)
        for row in dataset:
            self._map_column_names(row)
            self._clean_row(row)
            self._correct_columns(row)
            if row[COLUMN_TO_ADD_TO_GROUP.column1] and row[COLUMN_TO_ADD_TO_GROUP.column2]:
                row[COLUMN_TO_ADD_TO_GROUP.new_column] = f"{row[COLUMN_TO_ADD_TO_GROUP.column1]}" \
                                                         f"{config.DELIMITER}" \
                                                         f"{row[COLUMN_TO_ADD_TO_GROUP.column2]}"
            else:
                row[COLUMN_TO_ADD_TO_GROUP.new_column] = ''
            yield row

    def _correct_amount(self, amount):
        """Overrides _correct_amount to correct an amount field.
        Converts field amount to a Decimal object.
        """
        return Decimal(str(amount))

    @staticmethod
    def _correct_date(date):
        """Converts field date to the standard datetime object."""
        res = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ') if date else None
        return res
