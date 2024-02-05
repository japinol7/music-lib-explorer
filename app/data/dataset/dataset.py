from abc import ABCMeta, abstractmethod
from datetime import datetime
from itertools import groupby

from app.config import config
from app.tools.logger.logger import log


class Dataset(metaclass=ABCMeta):
    """Represents a dataset structured as a list of dictionaries."""

    def __init__(self, dataset):
        self.logger = log
        self.dataset = self._process(dataset)
        self.dataset_source = ''

    def get_grouped(self, key_group):
        """Gets the dataset grouped by a key which consist of a list of dictionaries with the dataset rows
        :return: A groupby object grouped by key_group.
        """
        def key_func(x):
            return x[key_group]

        return groupby(sorted(self.dataset, key=key_func), key_func)

    @abstractmethod
    def _process(self, dataset):
        """Processes the dataset as needed.
        This method is expected to be overridden by Dataset subclasses,
        which should transform the given dataset to a list of ordered dictionaries.
        """
        pass

    def _map_column_names(self, row):
        """Maps columns names so they will have the same name regardless of the dataset origin."""
        for key, n_key in zip([getattr(k, self.dataset_source) for k in config.COLUMNS_MAPPING.values()],
                              config.COLUMNS_MAPPING.keys()):
            row[n_key] = row.pop(key)

    def _clean_row(self, row):
        """Cleans a row getting rid of the unwanted columns."""
        unwanted_columns = set(row.keys()) - set(config.COLUMNS_MAPPING.keys())
        for unwanted_key in unwanted_columns:
            del row[unwanted_key]

    def _correct_columns(self, row):
        """Gets columns transformed to the correct object type."""
        self._remove_whitespace(row)
        for column in config.DATE_COLUMNS:
            row[column] = self._correct_date(row[column])
        for column in config.AMOUNT_COLUMNS:
            row[column] = self._correct_amount(row[column])

    def _remove_whitespace(self, row):
        """Removes all leading and trailing whitespaces from the configured columns."""
        for column in config.COLUMNS_TO_STRIP_WHITESPACE_FROM:
            row[column] = row[column].strip()

    @abstractmethod
    def _correct_amount(self, amount):
        """Converts amount field to a Decimal object correcting its separator if needed.
        This method is expected to be overridden by Dataset subclasses.
        It should transform the given amount to a Decimal object with the correct decimal separator.
        """
        pass

    @staticmethod
    def _correct_date(date):
        """Converts field date to the standard datetime object."""
        res = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.000000') if date else None
        return res
