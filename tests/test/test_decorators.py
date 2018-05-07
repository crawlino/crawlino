import pytest

from crawlino.decorators import crawlino_module
from crawlino.exceptions import CrawlinoValueError


def test_valid_decorator_usage():

    def _dummy_fn():
        pass

    dec = crawlino_module(module_type="input",
                          name="test",
                          output_types=["json"])

    f = dec(_dummy_fn)

    assert f.crawlino_module_name == "test"
    assert f.crawlino_module_type == "input"
    assert f.crawlino_module_output_types == ["json"]


def test_valid_decorator_invalid_module_type():

    def _dummy_fn():
        pass

    with pytest.raises(CrawlinoValueError):
        dec = crawlino_module(module_type="XXXX",
                              name="test",
                              output_types=["json"])
        f = dec(_dummy_fn)
