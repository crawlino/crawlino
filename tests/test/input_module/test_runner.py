from collections import Callable

from crawlino.crawlino import Crawlino


def test_input_module_has_callable_function(crawler_inline_definitions_path):
    c = Crawlino(crawler_inline_definitions_path)

    _ = next(c)  # Source step
    input_step = next(c)

    assert isinstance(input_step.calling_module, Callable)


def test_input_module_callable_fn_has_decorator(
        crawler_inline_definitions_path):

    c = Crawlino(crawler_inline_definitions_path)

    _ = next(c)  # Source step
    input_step = next(c)

    assert hasattr(input_step.calling_module, "crawlino_module_name")


def test_input_module_callable_fn_has_decorator_type_input(
        crawler_inline_definitions_path):

    c = Crawlino(crawler_inline_definitions_path)

    _ = next(c)  # Source step
    input_step = next(c)

    assert hasattr(input_step.calling_module, "crawlino_module_name")
    assert input_step.calling_module.crawlino_module_type == "input"


def test_input_module_callable_fn_has_decorator_module_name_rest(
        crawler_inline_definitions_path):

    c = Crawlino(crawler_inline_definitions_path)

    _ = next(c)  # Source step
    input_step = next(c)

    assert hasattr(input_step.calling_module, "crawlino_module_name")
    assert input_step.calling_module.crawlino_module_type == "input"
    assert input_step.calling_module.crawlino_module_name == "rest"


def test_input_module_call_run(
        crawler_inline_definitions_path):

    def _dummy(**kwargs):
        return "hello"

    c = Crawlino(crawler_inline_definitions_path)

    _ = next(c)  # Source step
    input_step = next(c)
    input_step.calling_module = _dummy

    assert input_step.run() == "hello"
