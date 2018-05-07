from crawlino import CrawlinoModel, CMModel, CMInput, CMExtractors, CMHooks, \
    CMSources, File


# --------------------------------------------------------------------------
# Loading and check types
# --------------------------------------------------------------------------
def test_load_model_crawler_ok(crawler_inline_definitions: File):
    assert isinstance(CrawlinoModel(crawler_inline_definitions), CrawlinoModel)


def test_load_crawler_name(crawler_inline_definitions: File):
    m = CrawlinoModel(crawler_inline_definitions)

    assert m.name == "myCrawler"


def test_load_model_crawler_sources(crawler_inline_definitions: File):
    m = CrawlinoModel(crawler_inline_definitions)

    assert isinstance(m.sources, CMSources)


def test_load_model_crawler_models(crawler_inline_definitions: File):
    m = CrawlinoModel(crawler_inline_definitions)

    assert isinstance(m.model, CMModel)


def test_load_model_crawler_models_import(crawler_import_definitions: File):
    m = CrawlinoModel(crawler_import_definitions)

    assert isinstance(m.model, CMModel)


def test_load_model_crawler_inputs(crawler_inline_definitions: File):
    m = CrawlinoModel(crawler_inline_definitions)

    assert isinstance(m.input, CMInput)


def test_load_model_crawler_crawler(crawler_inline_definitions: File):
    m = CrawlinoModel(crawler_inline_definitions)

    assert isinstance(m.crawlers, CMExtractors)


def test_load_model_crawler_hooks(crawler_inline_definitions: File):
    m = CrawlinoModel(crawler_inline_definitions)

    assert isinstance(m.hooks, CMHooks)
