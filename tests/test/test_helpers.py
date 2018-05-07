import os
import tempfile

from crawlino.helpers import gt, find_file


# --------------------------------------------------------------------------
# gt
# --------------------------------------------------------------------------
def test_gt_dict_return_ok():

    a = {"hello": "world"}

    assert gt(a, "hello", None) == "world"


def test_gt_dict_return_default():

    a = {"hello": "world"}

    assert gt(a, "xxx", "world") == "world"


def test_gt_non_dict_ok():

    a = 1

    assert gt(a, "xxx", "world") == 1


# --------------------------------------------------------------------------
# find_file
# --------------------------------------------------------------------------
def test_find_file_not_found():

    assert find_file("blah") is None


def test_find_file_absolute_path():
    with tempfile.NamedTemporaryFile() as f:
        assert find_file(f.name) == f.name


def test_find_file_current_dir():
    with tempfile.NamedTemporaryFile(dir=os.getcwd()) as f:
        curr_dir_file = os.path.join(os.getcwd(),
                                     f.name)

        assert find_file(os.path.basename(f.name)) == curr_dir_file
