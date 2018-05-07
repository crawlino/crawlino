
from crawlino_core.exceptions import CrawlinoValueError

from crawlino.helpers import gt
from crawlino.modules.config_module import CMConfig
from crawlino.modules.hooks_module.models import CMHook
from crawlino.modules.model_module.models import CMModel
from crawlino.modules.input_module.models import CMInput
from crawlino.modules.sources_module.models import CMSource
from crawlino.modules.extractors_module.models import CMRuleSet

from .input_model import File


class CrawlinoModel:

    def __init__(self, crawler_file: File):
        self.crawler_file = crawler_file
        self.name = gt(self.crawler_file.parsed, "name", None)
        self.description = gt(self.crawler_file.parsed, "description", "")
        self.tags = gt(self.crawler_file.parsed, "tags", [])

        if not self.name:
            raise CrawlinoValueError("Error in self.models: self.models must "
                                     "have 'name' property.")
        if not isinstance(self.tags, list) or \
                not all(isinstance(x, str) for x in self.tags):
            raise CrawlinoValueError("tags must be a list of strings")

        self.config = [
            CMConfig(type=x.get("type", None),
                     config=x.get("config", None),
                     name=x.get("name", None))
            for x in self.crawler_file.parsed.get("config", [])
        ]

        self.sources = [
            CMSource(type=x.get("type", None),
                     config=x.get("config", None),
                     name=x.get("name", None))
            for x in self.crawler_file.parsed.get("sources")
        ]

        self.model = [
            CMSource(type=x.get("type", None),
                     config=x.get("config", None),
                     name=x.get("name", None))
            for x in self.crawler_file.parsed.get("sources")
        ]

        _input = self.crawler_file.parsed.get("input")
        self.input = [CMInput(type=_input.get("type", None),
                              config=_input.get("config", None),
                              name=_input.get("name", None))]

        _extractors = self.crawler_file.parsed.get("extractors", {})
        self.extractors = [
            CMRuleSet(x.get("ruleSet"))
            for x in _extractors if "ruleSet" in x
        ]

        self.hooks = [
            CMHook(type=x.get("type", None),
                   config=x.get("config", None),
                   name=x.get("name", None))
            for x in self.crawler_file.parsed.get("hooks", [])
        ]
        # Setting default hook
        if not self.hooks:
            self.hooks = [CMHook(type="print", config=None, name=None)]

    @property
    def to_dict(self):
        return {}


__all__ = ("CrawlinoModel",)
