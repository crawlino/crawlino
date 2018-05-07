import json
import tempfile
from typing import Dict

import pytest

from crawlino import CrawlinoModel, CMModelsFields, CrawlinoFormatError, \
    CMModelsField, CrawlinoNotFoundError, CMModelsMappers, \
    CMModelsMappersObject, CrawlinoValueError, CMModel, CrawlinoStore, File


@pytest.fixture
def invalid_model_without_name() -> dict:
    return {
        "fields": [],
    }


@pytest.fixture
def check_model_fields_duplicate_names() -> File:

    with tempfile.NamedTemporaryFile() as f:
        ff = open(f.name, "w")
        json.dump({
            "type": "myCrawler",
            "sources": [
                {
                    "type": "my enumeration",
                    "type": "enumeration",
                    "config": {
                        "dataList": []
                    }
                }
            ],
            "model": {
                "type": "my_model_1",
                "fields": [
                    {
                        "type": "url",
                        "type": "text",
                    },

                    {
                        "type": "url",
                        "type": "text"
                    }
                ]
            }
        }, ff)
        ff.close()
        yield File(f.name)


@pytest.fixture
def check_model_mappers_invalid_format() -> File:

    with tempfile.NamedTemporaryFile() as f:
        ff = open(f.name, "w")
        json.dump({
            "type": "myCrawler",
            "sources": [
                {
                    "type": "my enumeration",
                    "type": "enumeration",
                    "config": {
                        "dataList": []
                    }
                }
            ],
            "model": {
                "type": "my_model_1",
                "mappers": [
                    {
                        "stdout": {
                            "type": "stdout1"
                        }
                    },
                    {
                        "bla": "asd",  # ERROR!
                        "raw": {
                            "type": "file type",
                            "path": "asdf"
                        }
                    }
                ]
            }
        }, ff)
        ff.close()
        yield File(f.name)


@pytest.fixture
def check_model_mappers_invalid_mapper() -> File:
    with tempfile.NamedTemporaryFile() as f:
        ff = open(f.name, "w")

        json.dump({
            "type": "myCrawler",
            "sources": [
                {
                    "type": "my enumeration",
                    "type": "enumeration",
                    "config": {
                        "dataList": []
                    }
                }
            ],
            "model": {
                "type": "my_model",
                "mappers": [
                    {
                        "stdout": {
                            "type": "stdout1"
                        }
                    },
                    {
                        "XXXX": {
                            "type": "file type",
                            "path": "asdf"
                        }
                    }
                ]
            }
        }, ff)
        ff.close()
        yield File(f.name)


# --------------------------------------------------------------------------
# Property: type
# --------------------------------------------------------------------------
def test_load_model_crawler_model_name(
        crawler_inline_definitions: CrawlinoStore):
    m = CrawlinoModel(crawler_inline_definitions)

    assert m.model.name == "my_model_1"


# --------------------------------------------------------------------------
# Property: fields
# --------------------------------------------------------------------------
def test_load_model_crawler_model_fields_check_type(
        crawler_inline_definitions: CrawlinoStore):

    m = CrawlinoModel(crawler_inline_definitions)

    assert isinstance(m.model.fields, CMModelsFields)


def test_load_model_crawler_model_fields_get(
        crawler_inline_definitions: CrawlinoStore):

    m = CrawlinoModel(crawler_inline_definitions)

    field_obj = m.model.fields.get("url")

    assert isinstance(field_obj, CMModelsField)

    assert field_obj.name == "url"
    assert field_obj.type == "text"
    assert field_obj.key == True


def test_load_model_crawler_model_fields_not_found(
        crawler_inline_definitions: CrawlinoStore):
    m = CrawlinoModel(crawler_inline_definitions)

    with pytest.raises(CrawlinoNotFoundError):
        m.model.fields.get("aaaa")


def test_load_model_crawler_model_fields_check_duplicates(
        check_model_fields_duplicate_names: File):

    with pytest.raises(CrawlinoFormatError):
        CrawlinoModel(check_model_fields_duplicate_names)


# --------------------------------------------------------------------------
# Property: mappers
# --------------------------------------------------------------------------
def test_load_model_crawler_model_mapper_check_type(
        crawler_inline_definitions: CrawlinoStore):

    m = CrawlinoModel(crawler_inline_definitions)

    assert isinstance(m.model.mappers, CMModelsMappers)


def test_load_model_crawler_model_mapper_loaded_maps(
        crawler_inline_definitions: CrawlinoStore):

    m = CrawlinoModel(crawler_inline_definitions)

    assert len(m.model.mappers.all()) == 4


def test_load_model_crawler_model_mapper_maps_types(
        crawler_inline_definitions: CrawlinoStore):

    m = CrawlinoModel(crawler_inline_definitions)

    assert all(isinstance(x, CMModelsMappersObject)
               for x in m.model.mappers.all()) == True


def test_load_model_crawler_model_mapper_check_format(
        check_model_mappers_invalid_format: File):

    with pytest.raises(CrawlinoFormatError):
        CrawlinoModel(check_model_mappers_invalid_format)


def test_load_model_crawler_model_mapper_invalid_mapper(
        check_model_mappers_invalid_mapper: File):

    with pytest.raises(CrawlinoValueError):
        CrawlinoModel(check_model_mappers_invalid_mapper)


def test_load_model_crawler_model_mapper_get_mapper(
        crawler_inline_definitions: CrawlinoStore):
    m = CrawlinoModel(crawler_inline_definitions)

    assert m.model.mappers.get("my_database").name == "my_database"


def test_load_model_crawler_model_mapper_get_mapper_non_exists(
        crawler_inline_definitions: CrawlinoStore):
    m = CrawlinoModel(crawler_inline_definitions)

    with pytest.raises(CrawlinoNotFoundError):
        m.model.mappers.get("XXXXX")


# --------------------------------------------------------------------------
# Inline models
# --------------------------------------------------------------------------
def test_load_model_ok(model_mock_001: Dict):
    assert isinstance(CMModel(model_mock_001), CMModel)


def test_load_model_name(model_mock_001: Dict):
    m = CMModel(model_mock_001)

    assert m.name == "my_model_1"


def test_load_model_no_name(invalid_model_without_name: Dict):

    with pytest.raises(CrawlinoValueError):
        CMModel(invalid_model_without_name)
