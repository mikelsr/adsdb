import configparser
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# import psycopg2.errors as errors
import pytest
from pymongo import MongoClient
from sqlalchemy import create_engine

from zones.utils import formatted_postgres_url

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


@pytest.fixture
def postgres_formatted_engine(formatted_config):
    # Use one engine to create the test database
    db_name = formatted_config["POSTGRES"]["FormattedDB"]
    conn = psycopg2.connect()
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    engine = create_engine(formatted_postgres_url(use_config=formatted_config))
    try:
        yield engine
    # Error will be raised if DB already exists
    # except errors.DuplicateDatabase:
    #     yield create_engine(formatted_postgres_url(use_config=formatted_config))
    finally:
        engine.dispose()
        # DROP TEST DATABASE
        conn.cursor().execute(f"DROP DATABASE {db_name};")
        conn.close()
