import os

from zones.formatted.formatter import Formatter
from zones.landing.fileresource import FileDataSource
from tests.conftest import test_data_path


def get_data_path():
    return test_data_path


_test_data_sources = [
    FileDataSource(filepath=os.path.join(get_data_path(), "Population-EstimatesData-1.csv")),
    FileDataSource(filepath=os.path.join(get_data_path(), "Population-EstimatesData-2.csv")),
]


def test_formatter_load(mongo_formatted_collection, formatted_config):

    # Populate the database and count the total number of rows added to it.
    rows = 0
    for data_source in _test_data_sources:
        data = data_source.load()
        rows += data.count("\n")
        data_source.store(data_source.wrap(data_source.load()), use_config=formatted_config)

    data = Formatter.load(use_config=formatted_config)

    assert len(data.index) == rows - 2
