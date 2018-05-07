import collections

from crawlino.crawlino import Crawlino
from crawlino.models import Runneable, CrawlinoModel
from crawlino.modules.input_module.runners import InputRunner
from crawlino.modules.model_module.runners import ModelRunner
from crawlino.modules.hooks_module.runners import HooksRunner
from crawlino.modules.sources_module.runners import SourcesRunner
from crawlino.modules.extractors_module.runners import ExtractorsRunner


def test_crawlino_load_models(crawler_inline_definitions_path):
    c = Crawlino(crawler_inline_definitions_path)

    assert isinstance(c.model, CrawlinoModel)


def test_crawlino_check_iterable(crawler_inline_definitions_path):
    c = Crawlino(crawler_inline_definitions_path)

    assert isinstance(c, collections.Iterable)


def test_crawlino_check_steps_number(crawler_inline_definitions_path):
    c = Crawlino(crawler_inline_definitions_path)

    assert len(list(c)) == 5


def test_crawlino_check_each_step_is_runneable(crawler_inline_definitions_path):
    c = Crawlino(crawler_inline_definitions_path)

    for x in c:
        assert isinstance(x, Runneable)


def test_crawlino_check_type_of_each_step(crawler_inline_definitions_path):
    c = Crawlino(crawler_inline_definitions_path)

    s0 = next(c)
    assert isinstance(s0, Runneable) and isinstance(s0, SourcesRunner)
    s1 = next(c)
    assert isinstance(s1, Runneable) and isinstance(s1, InputRunner)
    s2 = next(c)
    assert isinstance(s2, Runneable) and isinstance(s2, ExtractorsRunner)
    s3 = next(c)
    assert isinstance(s3, Runneable) and isinstance(s3, ModelRunner)
    s4 = next(c)
    assert isinstance(s4, Runneable) and isinstance(s4, HooksRunner)


def test_crawlino_check_ping_for_each_step(crawler_inline_definitions_path):
    c = Crawlino(crawler_inline_definitions_path)

    s0 = next(c)
    assert s0.ping() == "pong"
    s1 = next(c)
    assert s1.ping() == "pong"
    s2 = next(c)
    assert s2.ping() == "pong"
    s3 = next(c)
    assert s3.ping() == "pong"
    s4 = next(c)
    assert s4.ping() == "pong"


def test_crawlino_check_each_step_has_run_method(crawler_inline_definitions_path):
    c = Crawlino(crawler_inline_definitions_path)

    s0 = next(c)
    assert hasattr(s0, "run")
    s1 = next(c)
    assert hasattr(s1, "run")
    s2 = next(c)
    assert hasattr(s2, "run")
    s3 = next(c)
    assert hasattr(s3, "run")
    s4 = next(c)
    assert hasattr(s4, "run")


def test_crawlino_runs_all_steps(crawler_inline_definitions_path):
    class Dummy:

        def run(self):
            pass

    c = Crawlino(crawler_inline_definitions_path)
    c._models_map_ = [Dummy() for _ in range(len(c._models_map_))]
    c.run()

    assert c._step == 5

