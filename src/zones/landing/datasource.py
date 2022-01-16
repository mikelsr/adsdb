from abc import ABC, abstractmethod
from datetime import datetime
from pymongo import MongoClient

from zones.config import config


class DataSource(ABC):
    """DataSource is a class with abstract method and is not intended to be used directly,
    instead it should be inherited."""

    @abstractmethod
    def load(self) -> str:
        """Load data from the datasource in the form of io.TextIOBase. The implementation must be
        done by each specific datasource.

        :return: Loaded data in the form of io.TextIOBase.
        """
        pass

    @abstractmethod
    def origin(self) -> str:
        pass

    def wrap(self, data: str, metadata: dict = {}) -> dict:
        """Wrap the data in a dictionary object that contains both the data and metadata.

        :param origin: Origin of the data: a filepath, url...
        :param data: Actual data to wrap.
        :param metadata: Additional metadata fields that a child class can pass through, which will be merged
        with the existing metadata fields.
        :return: Dictionary object with the wrapped data.
        """
        assert self.origin() is not None and data is not None
        return {
            "metadata": {
                **metadata,
                **{
                    "origin": self.origin(),
                    "origin_class": self.__class__.__name__,
                    "datetime": datetime.now().strftime("%Y-%m-%dT%H-%M-%SZ"),
                },
            },
            "data": str(data),
        }

    def store(self, wrapped_data: dict, use_config=config):
        """Store wrapped data in persistent key-value storage using the origin and datetime as keys.

        :param wrapped_data: Data to be stored.
        :param use_config: Configuration to be used. Defaults to package configuration.
        :return: None.
        """
        assert wrapped_data is not None
        client = MongoClient(
            host=use_config["MONGO"]["Host"],
            port=int(use_config["MONGO"]["Port"]),
        )
        collection = client[use_config["MONGO"]["PersistentLandingDB"]][
            use_config["MONGO"]["PersistentLandingCollection"]
        ]
        collection.insert_one(wrapped_data)

    def run(self):
        """This method must load data, wrap it and store it, ideally in the following way:
        self.store(self.wrap(self.load()))"""
        self.store(self.wrap(self.load()))
