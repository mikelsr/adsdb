from typing import List

from landing.datasource import DataSource
from landing.filesystem import FileSystemDataSource
from landing.webresource import WebResourceDataSource

# TODO: config file (.py or .init?)


def run_once():
    datasources: List[DataSource] = [
        FileSystemDataSource(directory=''),
        WebResourceDataSource(url=''),
    ]

    # TODO: create run method for each data source instead of this
    # loop to be run constantly
    for datasource in datasources:
        datasource.load()
        datasource.wrap()  # ?
        datasource.store()



if __name__ == "__main__":
    run_once()
