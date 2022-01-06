import io
from abc import ABC, abstractmethod
from datetime import datetime
from json import dumps
from os import path
import redis

from zones.config import config


class DataSource(ABC):
    """DataSource is a class with abstract method and is not intended to be used directly,
    instead it should be inherited."""

    @abstractmethod
    def load(self) -> io.TextIOBase:
        """Load data from the datasource in the form of io.TextIOBase. The implementation must be
        done by each specific datasource.

        :return: Loaded data in the form of io.TextIOBase.
        """
        pass

    def wrap(self, origin: str, data: dict, metadata: dict = {}) -> dict:
        """Wrap the data in a dictionary object that contains both the data and metadata.

        :param origin: Origin of the data: a filepath, url...
        :param data: Actual data to wrap.
        :param metadata: Additional metadata fields that a child class can pass through, which will be merged
        with the existing metadata fields.
        :return: Dictionary object with the wrapped data.
        """
        assert origin is not None and data is not None
        return {
            "metadata": {
                **metadata,
                **{
                    "origin": origin,
                    "origin_class": self.__class__.__name__,
                    "datetime": datetime.now().strftime("%Y-%m-%dT%H-%M-%SZ"),
                },
            },
            "data": data,
        }

    def store(self, wrapped_data: dict):
        """Store wrapped data in persistent key-value storage using the origin and datetime as keys.

        :param wrapped_data: Data to be stored.
        :return: None.
        """
        assert wrapped_data is not None
        redis_connection = redis.Redis(
            host=config["REDIS"]["Host"], port=int(config["REDIS"]["Port"]), db=int(config["REDIS"]["Database"])
        )
        reduced_origin = path.basename(wrapped_data["metadata"]["origin"])
        k = f'{reduced_origin}_{wrapped_data["metadata"]["datetime"]}'
        v = dumps(wrapped_data)
        redis_connection.set(k, v)

    @abstractmethod
    def run(self):
        """This method must load data, wrap it and store it, ideally in the following way:
        self.store(self.wrap(self.load()))"""
        pass
