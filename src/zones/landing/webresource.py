from urllib.request import urlopen

from zones.landing.datasource import DataSource


class WebResourceDataSource(DataSource):
    """WebResourceDataSource is used to load data from files accessible via web URLs."""

    def __init__(self, url: str) -> None:
        """Class constructor.

        :param url: URL of the datasource.
        """
        self._url = url

    def load(self):
        with urlopen(self._url) as f:
            return f.read()

    def run(self):
        self.store(self.wrap(self.load()))
