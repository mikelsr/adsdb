from pymongo import MongoClient

from zones.config import config


def persistent_mongodb_collection(use_config=config):
    """Return collection used for the persistent storage stage.

    :param use_config: Config to be used, zones.config.config by default.
    :return: Collection used for persistent storage.
    """
    client = MongoClient(host=use_config["MONGO"]["Host"], port=int(use_config["MONGO"]["Port"]))
    db_name = use_config["MONGO"]["PersistentLandingDB"]
    collection_name = use_config["MONGO"]["PersistentLandingCollection"]
    collection = client[db_name][collection_name]
    return collection
