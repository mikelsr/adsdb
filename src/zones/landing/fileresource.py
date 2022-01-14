import io

from zones.landing.datasource import DataSource


class FileDataSource(DataSource):
    """FileDataSource is used to load data from files accessible in the filesystem."""

    def __init__(self, filepath: str) -> None:
        """Class constructor.

        :param filepath: Filepath of the datasource.
        """
        self._filepath = filepath

    def origin(self) -> str:
        assert self._filepath is not None
        return self._filepath

    def load(self) -> str:
        """
        Load data from the file of the FileDataSource.
        :return: Raw data in the form of io.TextIOBase.
        """
        with open(self._filepath, "r") as data:
            return str(data.read())

    def wrap(self, data: dict) -> dict:
        """Wrap data using DataSource.wrap passing the filepath as origin.

        :param data: Raw data to wrap.
        :return: Dictionary object containing the wrapped data.
        """
        return super().wrap(data=data)

    def run(self):
        self.store(self.wrap(self.load()))
