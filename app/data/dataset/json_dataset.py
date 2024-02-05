from decimal import Decimal
from collections import OrderedDict

from app.config import config
from app.data.dataset.dataset import Dataset


class JsonDataset(Dataset):
    """Represents a json a dataset structured as a list of dictionaries."""

    def __init__(self, dataset):
        super().__init__(dataset)
        self.dataset_source = config.DATASET_SOURCE_JSON
        self.logger.debug('Reading a json dataset')

    def _process(self, dataset):
        """Overrides _process to process the dataset from a json resource.
        Transforms the given dataset to a list of ordered dictionaries.
        """
        dataset = (OrderedDict(x.items()) for x in dataset)
        for row in dataset:
            self._map_column_names(row)
            self._clean_row(row)
            self._correct_columns(row)
            yield row

    def _correct_amount(self, amount):
        """Overrides _correct_amount to correct an amount field.
        Converts field amount to a Decimal object.
        """
        return Decimal(str(amount))
