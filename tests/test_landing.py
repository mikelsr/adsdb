import pytest
from typing import List

from zones.landing.datasource import DataSource
from zones.landing.fileresource import FileDataSource
from zones.landing.webresource import WebResourceDataSource


@pytest.fixture
def data_sources() -> List[DataSource]:
    return [
        FileDataSource(filepath="/Users/mikel/Code/github.com/mikelsr/adsdb/data/Population-EstimatesData-1.csv"),
        WebResourceDataSource(url="https://adsdb.mikel.xyz/Population-EstimatesData-2.csv"),
    ]


def test_datasources_load(data_sources):
    for data_source in data_sources:
        assert data_source.load() is not None
