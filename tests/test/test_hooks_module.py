import io
import json
import pytest

from io import TextIOWrapper

from crawlino import CrawlinoModel, CMHook


@pytest.fixture
def invalid_types() -> dict:
    with io.TextIOWrapper(io.BytesIO()) as f:
        json.dump({
            "type": "myCrawler",
            "config": {
            },
            "input": {
                "type": "rest",
                "config": {}
            },
            "hooks": [
                {
                    "type": "xxxx",
                    "config": {}
                }
            ]
        }, f)
        f.seek(0)
        yield f


# --------------------------------------------------------------------------
# hooks.get_list()
# --------------------------------------------------------------------------
def test_load_hooks_inline_ok(crawler_inline_definitions: TextIOWrapper):
    m = CrawlinoModel(crawler_inline_definitions)

    assert isinstance(m.hooks.get_list(), list)


def test_load_hooks_import_ok(crawler_import_definitions: TextIOWrapper):
    m = CrawlinoModel(crawler_import_definitions)

    assert isinstance(m.hooks.get_list(), list)


def test_load_hooks_inline_check_hooks_types(crawler_inline_definitions: TextIOWrapper):
    m = CrawlinoModel(crawler_inline_definitions)

    v = all(isinstance(x, CMHook) for x in m.hooks.get_list())

    assert len(m.hooks.get_list()) > 0 and v is True


def test_load_hooks_import_check_hooks_types(crawler_import_definitions: TextIOWrapper):
    m = CrawlinoModel(crawler_import_definitions)

    v = all(isinstance(x, CMHook) for x in m.hooks.get_list())

    assert len(m.hooks.get_list()) > 0 and v is True


