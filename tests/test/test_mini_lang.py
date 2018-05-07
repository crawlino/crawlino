import pytest

from os.path import join, dirname, abspath

from crawlino.exceptions import CrawlinoNotFoundError
from crawlino.mini_lang import do_script, MODEL_FUNCTION_MAPPING, import_action


@pytest.fixture
def crawler_import_definitions_path() -> str:

    return join(abspath(join(dirname(__file__), "..")), "mocks/")


# --------------------------------------------------------------------------
# do_script
# --------------------------------------------------------------------------
def test_do_script_non_text_ok():
    assert do_script({}) == {}


def test_do_script_text_invalid_action():
    with pytest.raises(CrawlinoNotFoundError):
        do_script("@asdf")


def test_do_script_text_run_script_no_params():
    def _custom(*args):
        return "hello"

    MODEL_FUNCTION_MAPPING["my_func"] = _custom

    assert do_script("@my_func") == "hello"


def test_do_script_text_run_script_params():
    def _custom(*args):
        return args[1]

    MODEL_FUNCTION_MAPPING["my_func"] = _custom

    assert do_script("@my_func(hello)") == "hello"


# --------------------------------------------------------------------------
# SCRIPT: @import(...) -> import_action
# --------------------------------------------------------------------------
def test_import_action_runs_ok(crawler_import_definitions_path):
    r = import_action(crawler_import_definitions_path,
                      *["crawler_with_imports.json"])

    assert type(r) is dict


def test_import_action_runs_no_json_extension(crawler_import_definitions_path):
    r = import_action(crawler_import_definitions_path,
                      *["crawler_with_imports"])

    assert type(r) is dict
