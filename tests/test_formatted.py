import os
import pandas as pd
import pytest

# from sqlalchemy import create_engine
from zones.formatted.formatter import Formatter
from zones.landing.fileresource import FileDataSource
from zones.utils import postgres_select_query
from tests.conftest import test_data_path


def get_data_path():
    return test_data_path


_test_data_sources = [
    FileDataSource(filepath=os.path.join(get_data_path(), "Population-EstimatesData-1.csv")),
    FileDataSource(filepath=os.path.join(get_data_path(), "Population-EstimatesData-2.csv")),
]


def test_formatter_load_store(mongo_formatted_collection, formatted_config, postgres_formatted_engine):

    # Populate the database and count the total number of rows added to it.
    rows = 0
    for data_source in _test_data_sources:
        data = data_source.load()
        rows += data.count("\n")
        data_source.store(data_source.wrap(data_source.load()), use_config=formatted_config)

    data = Formatter.load(use_config=formatted_config)

    assert len(data.index) == rows - 2

    try:
        Formatter.store(data, use_config=formatted_config)
    except ValueError as e:
        pytest.fail(str(e))

    result = pd.read_sql_query(postgres_select_query(formatted_config), con=postgres_formatted_engine)

    # Remove index column created for postgres
    result.drop("index", axis=1, inplace=True)

    assert data.shape == result.shape
