from urllib.request import urlopen

from zones.landing.datasource import DataSource


class WebResourceDataSource(DataSource):
    """WebResourceDataSource is used to load data from files accessible via web URLs."""

    def __init__(self, url: str) -> None:
        """Class constructor.

        :param url: URL of the datasource.
        """
        self._url = url

    def origin(self) -> str:
        assert self._url is not None
        return self._url

    def load(self) -> str:
        with urlopen(self._url) as f:
            return str(f.read())

    def run(self):
        self.store(self.wrap(self.load()))
