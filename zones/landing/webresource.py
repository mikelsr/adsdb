from landing.datasource import DataSource

# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler

# TODO: find a good way to specify the persistent directory root

class WebResourceDataSource(DataSource):
    def __init__(self, target:str, url: str) -> None:
        self._url = url

    def load():
        pass

    def wrap():
        pass

    def store():
        pass
