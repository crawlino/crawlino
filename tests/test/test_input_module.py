import io
import json
import tempfile

import pytest

from io import TextIOWrapper
from crawlino import CMInput, CrawlinoModel, CrawlinoValueError, File
from crawlino.modules_stores import CrawlinoModulesStore


@pytest.fixture
def input_without_type() -> File:

    with tempfile.NamedTemporaryFile() as f:
        ff = open(f.name, "w")
        json.dump({
            "type": "myCrawler",
            "config": {
            },
            "sources": [
                {
                    "type": "my enumeration",
                    "type": "enumeration",
                    "config": {
                        "dataList": []
                    }
                }
            ],
            "input": {
                "config": {}
            }
        }, ff)
        ff.close()
        yield File(f.name)


@pytest.fixture
def input_without_config() -> File:

    with tempfile.NamedTemporaryFile() as f:
        ff = open(f.name, "w")
        json.dump({
            "type": "myCrawler",
            "config": {
            },
            "sources": [
                {
                    "type": "my enumeration",
                    "type": "enumeration",
                    "config": {
                        "dataList": []
                    }
                }
            ],
            "input": {
                "type": "rest"
            }
        }, ff)
        ff.close()
        yield File(f.name)


@pytest.fixture
def invalid_types() -> File:

    with tempfile.NamedTemporaryFile() as f:
        ff = open(f.name, "w")
        json.dump({
            "type": "myCrawler",
            "config": {
            },
            "sources": [
                {
                    "type": "my enumeration",
                    "type": "enumeration",
                    "config": {
                        "dataList": []
                    }
                }
            ],
            "input": {
                "type": "xxxx",
                "config": {}
            }
        }, ff)
        ff.close()
        yield File(f.name)


# --------------------------------------------------------------------------
# Loading and check types
# --------------------------------------------------------------------------
def test_load_input_inline_ok(crawler_inline_definitions: File):
    m = CrawlinoModel(crawler_inline_definitions)

    assert isinstance(m.input, CMInput)


def test_load_input_import_ok(crawler_import_definitions: File):
    m = CrawlinoModel(crawler_import_definitions)

    assert isinstance(m.input, CMInput)


def test_load_input_import_not_type(crawler_inline_definitions: File):
    m = CrawlinoModel(crawler_inline_definitions)

    assert hasattr(m.input, "type")


def test_load_input_inline_not_type(crawler_import_definitions: File):
    m = CrawlinoModel(crawler_import_definitions)

    assert hasattr(m.input, "type")


def test_load_input_import_not_config(crawler_inline_definitions: File):
    m = CrawlinoModel(crawler_inline_definitions)

    assert hasattr(m.input, "config")


def test_load_input_inline_not_config(crawler_import_definitions: File):
    m = CrawlinoModel(crawler_import_definitions)

    assert hasattr(m.input, "config")


def test_load_input_import_check_valid_types(crawler_inline_definitions: File):
    m = CrawlinoModel(crawler_inline_definitions)

    assert CrawlinoModulesStore.find_module("input", m.input.type) is not None


def test_load_input_inline_check_valid_types(crawler_import_definitions: File):
    m = CrawlinoModel(crawler_import_definitions)

    assert CrawlinoModulesStore.find_module("input", m.input.type) is not None


def test_load_input_raises_invalid_valid_types(invalid_types: File):

    with pytest.raises(CrawlinoValueError):
        CrawlinoModel(invalid_types)


def test_input_without_type(input_without_type: File):

    with pytest.raises(CrawlinoValueError):
        CrawlinoModel(input_without_type)


def test_input_without_config(input_without_config: File):

    with pytest.raises(CrawlinoValueError):
        CrawlinoModel(input_without_config)
