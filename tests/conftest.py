import os
import pytest
from pymongo import MongoClient

import zones.config as original_config


test_path = os.path.dirname(os.path.abspath(__file__))
test_data_path = os.path.join(test_path, "data")


@pytest.fixture
def config():
    test_config_ini = os.path.join(test_path, "config.ini")
    original_config.reload(test_config_ini)

    yield original_config.config


@pytest.fixture
def mongo_collection(config):
    """Fixture for the mongo collection used for landing tests."""
    # Get collection used for test persistent storage.
    # It is done manually in order to use the client in the tear-down.
    client = MongoClient(host=config["MONGO"]["Host"], port=int(config["MONGO"]["Port"]))
    db_name = config["MONGO"]["PersistentLandingDB"]
    collection_name = config["MONGO"]["PersistentLandingCollection"]
    collection = client[db_name][collection_name]

    yield collection

    # Drop test table
    client.drop_database(db_name)
