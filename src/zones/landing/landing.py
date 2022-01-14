from typing import List

from zones.landing.datasource import DataSource
from zones.landing.webresource import WebResourceDataSource
from zones.landing.fileresource import FileDataSource


def run_once():
    datasources: List[DataSource] = [
        FileDataSource(filepath="/home/mikel/Code/github.com/mikelsr/adsdb/data/Population-EstimatesData-1.csv"),
        WebResourceDataSource(url="https://adsdb.mikel.xyz/Population-EstimatesData-2.csv"),
    ]

    # TODO: create run method for each data source instead of this
    # loop to be run constantly
    for datasource in datasources:
        datasource.store(datasource.wrap(datasource.load()))


if __name__ == "__main__":
    run_once()
