import os
import io
import json
import pytest
import tempfile

from crawlino.exceptions import CrawlinoFormatError
from crawlino.models import CrawlinoStore, File


@pytest.fixture
def crawlino_base_dir() -> dict:

    with tempfile.TemporaryDirectory() as d:

        yield d


@pytest.fixture
def crawlino_base_dir_with_info() -> dict:

    with tempfile.TemporaryDirectory(prefix="/tmp/") as d:

        w_dir = os.path.join(d, "my_crawler.json")
        open(w_dir, "w").write("""
  {
    "type": "myCrawler",
    "config": {
      "logger": "mylogger",
      "sentryDSN": "asdf",
      "remoteLoggerDSN": ""
    },
    "sources": [
      {
        "type": "dummySource",
        "type": "dummy",
        "config": {
          "dataList": []
        }
      }
    ],
    "input": {
      "type": "rest",
      "config": {
        "httpMethod": "GET",
        "httpType": "json",
        "httpHeaders": {
          "header1": "$VAR$",
          "header2": "value2"
        },
        "data": "my=ad5a&asdf=asdf"
      }
    },
    "hooks": [
      {
        "type": "slack",
        "config": {
          "param1": "value1"
        }
      }
    ]
  }
            
        """)

        yield d


@pytest.fixture
def json_example_file() -> dict:

    with io.TextIOWrapper(io.BytesIO()) as f:
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
        }, f)
        f.seek(0)

        yield File(path="/tmp/config.js", name="config.js", file_handler=f)


@pytest.fixture
def yaml_example_file() -> dict:
    d = """
type: myCrawler
config: {}
sources:
- type: my enumeration
  type: enumeration
  config:
    dataList: []
input:
  type: rest
  config: {}
"""
    with io.TextIOWrapper(io.BytesIO()) as f:
        f.write(d)
        f.seek(0)

        yield File(path="/tmp/config.yaml", name="config.yaml", file_handler=f)


# --------------------------------------------------------------------------
# CrawlinoStore: constructor
# --------------------------------------------------------------------------
def test_crawlino_input_config_empty_input():
    c = CrawlinoStore()

    assert len(c.paths) == 2
    assert len(c.dirs) == 1


def test_crawlino_input_config_empty_dir(crawlino_base_dir):
    c = CrawlinoStore(crawlino_base_dir)

    assert len(c.paths) == 0
    assert len(c.dirs) == 0


def test_crawlino_input_config_with_info(crawlino_base_dir_with_info):
    c = CrawlinoStore(crawlino_base_dir_with_info)

    assert len(c.paths) == 1
    assert len(c.dirs) == 1


# --------------------------------------------------------------------------
# File: file_type
# --------------------------------------------------------------------------
def test_input_module_file_none_input(json_example_file: File):
    with pytest.raises(CrawlinoFormatError):
        File(None)


def test_input_module_file_load_path_and_name(json_example_file: File):
    p = "/tmp/my_file.json"

    with tempfile.NamedTemporaryFile(suffix="json") as f:

        o = File(f.name)

        assert o.path == f.name
        assert o.name == os.path.basename(f.name)


def test_input_module_file_json_parse_type_ok(json_example_file: File):
    assert type(json_example_file.parsed) is dict


def test_input_module_file_json_parse_data_ok(json_example_file: File):
    d = json_example_file.parsed

    assert "type" in d
    assert "config" in d
    assert "sources" in d
    assert "input" in d


def test_input_module_file_json_file_type(json_example_file: File):
    assert json_example_file.file_type == "json"


def test_input_module_file_yaml_parse_type_ok(yaml_example_file: File):
    assert type(yaml_example_file.parsed) is dict


def test_input_module_file_yaml_parse_data_ok(yaml_example_file: File):
    d = yaml_example_file.parsed

    assert "type" in d
    assert "config" in d
    assert "sources" in d
    assert "input" in d


def test_input_module_file_yaml_file_type(yaml_example_file: File):
    assert yaml_example_file.file_type == "yaml"
