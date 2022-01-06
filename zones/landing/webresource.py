from urllib.request import urlopen

from zones.landing.datasource import DataSource


# TODO: find a good way to specify the persistent directory root


class WebResourceDataSource(DataSource):
    def __init__(self, url: str) -> None:
        self._url = url

    def load(self):
        with urlopen(self._url) as f:
            return f.read()

    def wrap(self):
        pass
