from configparser import ConfigParser
import os
from pymongo.collection import Collection
import pytest


from zones.landing.datasource import DataSource
from zones.landing.fileresource import FileDataSource
from zones.landing.webresource import WebResourceDataSource

from tests.conftest import test_data_path


def get_data_path():
    return test_data_path


_test_data_sources = [
    FileDataSource(filepath=os.path.join(get_data_path(), "Population-EstimatesData-1.csv")),
    WebResourceDataSource(url="https://adsdb.mikel.xyz/Population-EstimatesData-2.csv"),
]


@pytest.mark.parametrize("data_source", _test_data_sources)
def test_data_sources(data_source, landing_config, mongo_landing_collection):
    data = _test_data_sources_load(data_source)
    wrapped_data = _test_data_sources_wrap(data_source, data)
    _test_data_sources_store(data_source, wrapped_data, landing_config, mongo_landing_collection)


def _test_data_sources_load(data_source: DataSource) -> str:
    data = data_source.load()
    assert data is not None
    return data


def _test_data_sources_wrap(data_source: DataSource, data: str) -> dict:
    wrapped_data = data_source.wrap(data)
    assert wrapped_data is not None
    for k, v in wrapped_data.items():
        if type(v) is dict:
            for sv in v.values():
                assert sv is not None
        else:
            assert v is not None
    return wrapped_data


def _test_data_sources_store(
    data_source: DataSource, wrapped_data: dict, test_config: ConfigParser, mongo_collection: Collection
):
    data_source.store(wrapped_data, use_config=test_config)
    stored_item = mongo_collection.find_one(
        {
            "metadata.origin": wrapped_data["metadata"]["origin"],
            "metadata.datetime": wrapped_data["metadata"]["datetime"],
        }
    )

    assert stored_item.get("metadata") == wrapped_data.get("metadata")
    assert stored_item.get("data") == wrapped_data.get("data")
