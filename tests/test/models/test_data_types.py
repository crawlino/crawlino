import pytest

from crawlino.models import SimpleListPluginData


# --------------------------------------------------------------------------
# SimpleListPluginData: Constructor
# --------------------------------------------------------------------------
def test_simple_data_types_ok():
    c = SimpleListPluginData(["hello", "world"])

    assert type(c) is SimpleListPluginData


def test_simple_data_types_empty_input():

    with pytest.raises(TypeError):
        SimpleListPluginData()


def test_simple_data_types_none_input():
    c = SimpleListPluginData(None)

    assert c.data == []


# --------------------------------------------------------------------------
# SimpleListPluginData: __eq__
# --------------------------------------------------------------------------
def test_simple_data_types__eq__ok():
    assert SimpleListPluginData([1, 2]) == SimpleListPluginData([2, 1])


def test_simple_data_types__eq__invalid_type():
    c = SimpleListPluginData([1, 2]) == 1
    assert c is False


def test_simple_data_types__eq__invalid_module_name():
    c = SimpleListPluginData([1, 2])
    c.module_name = "asdf"

    e = c == SimpleListPluginData([2, 1])

    assert e is False
