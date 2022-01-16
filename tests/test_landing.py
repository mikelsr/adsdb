from configparser import ConfigParser
import os
from pymongo import MongoClient
from pymongo.collection import Collection
import pytest

import zones.config as original_config
from zones.landing.datasource import DataSource
from zones.landing.fileresource import FileDataSource
from zones.landing.webresource import WebResourceDataSource


_test_path = os.path.dirname(os.path.abspath(__file__))
_test_data_path = os.path.join(_test_path, "data")
_test_data_sources = [
    FileDataSource(
        filepath=os.path.join(_test_data_path, "Population-EstimatesData-1.csv")
    ),
    WebResourceDataSource(url="https://adsdb.mikel.xyz/Population-EstimatesData-2.csv"),
]


@pytest.fixture
def config():
    test_config_ini = os.path.join(_test_path, "config.ini")
    original_config.reload(test_config_ini)

    yield original_config.config


@pytest.fixture
def mongo_collection(config):
    """Fixture for the mongo collection used for landing tests."""
    client = MongoClient(
        host=config["MONGO"]["Host"],
        port=int(config["MONGO"]["Port"]),
    )

    # Extract collection from client
    db_name = config["MONGO"]["PersistentLandingDB"]
    collection_name = config["MONGO"]["PersistentLandingCollection"]
    collection = client[db_name][collection_name]

    yield collection

    # Drop test table
    client.drop_database(db_name)


@pytest.mark.parametrize("data_source", _test_data_sources)
def test_data_sources(data_source, config, mongo_collection):
    data = _test_data_sources_load(data_source)
    wrapped_data = _test_data_sources_wrap(data_source, data)
    _test_data_sources_store(data_source, wrapped_data, config, mongo_collection)


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
    data_source: DataSource,
    wrapped_data: dict,
    test_config: ConfigParser,
    mongo_collection: Collection,
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
