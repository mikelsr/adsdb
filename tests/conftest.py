import configparser
import os
import pytest
from pymongo import MongoClient


test_path = os.path.dirname(os.path.abspath(__file__))
test_data_path = os.path.join(test_path, "data")


@pytest.fixture
def landing_config():
    config = configparser.ConfigParser()
    test_config_ini = os.path.join(test_path, "config", "landing.ini")
    config.read(test_config_ini)

    yield config


@pytest.fixture
def formatted_config():
    config = configparser.ConfigParser()
    test_config_ini = os.path.join(test_path, "config", "formatted.ini")
    config.read(test_config_ini)

    yield config


def _mongo_collection(config):
    # Get collection used for test persistent storage.
    # It is done manually in order to use the client in the tear-down.
    client = MongoClient(host=config["MONGO"]["Host"], port=int(config["MONGO"]["Port"]))
    db_name = config["MONGO"]["PersistentLandingDB"]
    collection_name = config["MONGO"]["PersistentLandingCollection"]
    collection = client[db_name][collection_name]
    return collection, db_name, client


@pytest.fixture
def mongo_landing_collection(landing_config):
    """Fixture for the mongo collection used for landing tests."""
    collection, db_name, client = _mongo_collection(landing_config)

    yield collection

    # Drop test table
    client.drop_database(db_name)


@pytest.fixture
def mongo_formatted_collection(formatted_config):
    """Fixture for the mongo collection used for formatted tests."""
    collection, db_name, client = _mongo_collection(formatted_config)

    yield collection

    # Drop test table
    client.drop_database(db_name)
