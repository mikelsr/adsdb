from abc import ABC, abstractclassmethod


class DataSource(ABC):
    @abstractclassmethod
    def load():
        pass

    @abstractclassmethod
    def wrap():
        pass

    @abstractclassmethod
    def store():
        pass

