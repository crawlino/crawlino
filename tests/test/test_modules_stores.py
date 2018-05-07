from crawlino.modules_stores import CrawlinoModulesStore


# --------------------------------------------------------------------------
# CrawlinoModulesStore.get_all_plugin_paths()
# --------------------------------------------------------------------------
def test_get_all_plugin_paths_oks():
    assert isinstance(CrawlinoModulesStore.get_all_python_files(), dict)


def test_get_all_plugin_paths_not_contains__init__():
    assert all("__init__.py" not in x for x in CrawlinoModulesStore.get_all_python_files())


# --------------------------------------------------------------------------
# CrawlinoModulesStore.load_plugins()
# --------------------------------------------------------------------------
def test_load_plugins_oks():
    CrawlinoModulesStore.load_modules()

    assert CrawlinoModulesStore.modules.get("input") is not None

