from landing.datasource import DataSource

# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler

# TODO: find a good way to specify the persistent directory root

class FileSystemDataSource(DataSource):
    def __init__(self, target:str, directory: str) -> None:
        self._dir = directory

    def load():
        pass

    def wrap():
        pass

    def store():
        pass
