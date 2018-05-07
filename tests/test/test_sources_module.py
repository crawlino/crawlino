import json
import pytest
import tempfile

from collections import Iterable

from crawlino import CMSources, CMSource, CrawlinoModel, CrawlinoValueError, \
    File


@pytest.fixture
def input_without_type() -> File:

    with tempfile.NamedTemporaryFile() as f:
        ff = open(f.name, "w")
        json.dump({
            "type": "myCrawler",
            "config": {
            },
            "sources": {
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
            "sources": {
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
            "sources": {
                "type": "xxxx",
                "config": {}
            }
        }, ff)
        ff.seek(0)
        yield File(f.name)


@pytest.fixture
def empty_sources() -> File:
    with tempfile.NamedTemporaryFile() as f:
        ff = open(f.name, "w")
        json.dump({
            "type": "myCrawler",
            "config": {
            }
        }, ff)
        ff.close()
        yield File(f.name)


# --------------------------------------------------------------------------
# Loading and check types
# --------------------------------------------------------------------------
def test_sources_inline_ok(crawler_inline_definitions: File):
    m = CrawlinoModel(crawler_inline_definitions)

    assert isinstance(m.sources, CMSources)


def test_sources_import_ok(crawler_import_definitions: File):
    m = CrawlinoModel(crawler_import_definitions)

    assert isinstance(m.sources, CMSources)


def test_sources_import_type_is_list(crawler_inline_definitions: File):
    m = CrawlinoModel(crawler_inline_definitions)

    assert isinstance(m.sources.get_list(), list)


def test_sources_empty_sources(empty_sources: File):

    with pytest.raises(CrawlinoValueError):
        CrawlinoModel(empty_sources)


def test_sources_import_not_type(crawler_inline_definitions: File):
    m = CrawlinoModel(crawler_inline_definitions)

    assert isinstance(m.sources.get_list(), list)


def test_sources_check_each_element_type(crawler_import_definitions: File):
    m = CrawlinoModel(crawler_import_definitions)

    r = list(isinstance(x, CMSource) for x in m.sources.get_list())
    assert len(r) != 0 and all(r) is True


def test_sources_find_element(crawler_import_definitions: File):
    m = CrawlinoModel(crawler_import_definitions)

    assert isinstance(m.sources.find("dummySource"), CMSource)


def test_sources_check_is_iterable(crawler_import_definitions: File):
    m = CrawlinoModel(crawler_import_definitions)

    assert isinstance(m.sources, Iterable)


def test_sources_check_iteration(crawler_import_definitions: File):
    m = CrawlinoModel(crawler_import_definitions)

    content = list(m.sources)

    assert len(content) > 0 and all(isinstance(x, CMSource) for x in content)


