import os
import pytest

from zones.landing.fileresource import FileDataSource
from zones.landing.webresource import WebResourceDataSource


_test_path = os.path.dirname(os.path.abspath(__file__))
_test_data_path = os.path.join(_test_path, "data")
_test_data_sources = [
    FileDataSource(filepath=os.path.join(_test_data_path, "Population-EstimatesData-1.csv")),
    WebResourceDataSource(url="https://adsdb.mikel.xyz/Population-EstimatesData-2.csv"),
]


@pytest.mark.parametrize("data_source", _test_data_sources)
def test_data_sources_load(data_source):
    assert data_source.load() is not None
