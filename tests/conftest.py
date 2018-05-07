import json

import pytest

from typing import Dict
from io import TextIOWrapper
from os.path import abspath, join, dirname

from crawlino import CrawlinoStore, File


@pytest.fixture
def model_mock_001() -> Dict:

    f = join(abspath(dirname(__file__)),
             "mocks",
             "model_001.json")

    return json.load(open(f))


@pytest.fixture
def crawler_inline_definitions() -> File:

    f = join(abspath(dirname(__file__)),
             "mocks",
             "crawler_inline_definitions.json")

    return File(f)


@pytest.fixture
def crawler_inline_definitions_path() -> File:

    f = join(abspath(dirname(__file__)),
             "mocks",
             "crawler_inline_definitions.json")

    return File(f)


@pytest.fixture
def crawler_import_definitions() -> File:

    f = join(abspath(dirname(__file__)),
             "mocks",
             "crawler_with_imports.json")

    return File(f)
