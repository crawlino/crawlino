import json
import pytest
import tempfile

from crawlino import CMConfig, CrawlinoModel, File


@pytest.fixture
def generic_logger_name() -> File:

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
                "type": "rest",
                "config": {}
            }
        }, ff)
        ff.close()
        yield File(f.name)


# --------------------------------------------------------------------------
# Loading and check types
# --------------------------------------------------------------------------
def test_load_config_ok(crawler_inline_definitions: File):
    m = CrawlinoModel(crawler_inline_definitions)

    assert isinstance(m.config, CMConfig)


def test_load_config_generic_logger_name(generic_logger_name: File):
    m = CrawlinoModel(generic_logger_name)

    assert m.config.logger == "crawlino"


def test_load_config_custom_logger_name_import(crawler_import_definitions: File):
    m = CrawlinoModel(crawler_import_definitions)

    assert m.config.logger == "mylogger"


def test_load_config_custom_logger_name_inline(crawler_inline_definitions: File):
    m = CrawlinoModel(crawler_inline_definitions)

    assert m.config.logger == "mylogger"

