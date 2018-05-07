from crawlino.crawlino import Crawlino
from crawlino.models import SimpleListPluginData


# --------------------------------------------------------------------------
# SourcesRunner: run
# --------------------------------------------------------------------------
def test_sources_run_returns_list(crawler_inline_definitions_path):
    c = Crawlino(crawler_inline_definitions_path)

    sources_step = next(c)

    assert isinstance(sources_step.run(), list)


def test_sources_run_return_valid_data_types(crawler_inline_definitions_path):
    c = Crawlino(crawler_inline_definitions_path)

    sources_step = next(c)

    runs_returns = sources_step.run()

    assert len(runs_returns) > 0 and all(
        isinstance(x, SimpleListPluginData) for x in runs_returns)


def test_sources_run_return_valid_data_values(crawler_inline_definitions_path):
    c = Crawlino(crawler_inline_definitions_path)

    sources_step = next(c)

    runs_returns = sources_step.run()
    dummy_module_return = SimpleListPluginData("dummy module runs!".split())
    dummy_module_return.module_name = "dummy_module"

    assert all(x == dummy_module_return
               for x in runs_returns if x.module_name == "dummy_module")


def test_sources_run_run_only_selected_modules(crawler_inline_definitions_path):
    c = Crawlino(crawler_inline_definitions_path)

    sources_step = next(c)

    runs_returns = sources_step.run(only_these_modules=["XXXXXX"])

    assert len(runs_returns) == 0



