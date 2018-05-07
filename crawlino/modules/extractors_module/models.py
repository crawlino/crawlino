from typing import Dict
from collections import OrderedDict

from crawlino_core import STEP_EXTRACTOR, un_camel, CrawlinoValueError
from crawlino_core.modules_stores import CrawlinoModulesStore

from crawlino.models import CModelBase, CModelBaseLoader


class CMRule(CModelBase, metaclass=CModelBaseLoader):

    __slots__ = ("type", "config", "name")

    def __init__(self, type: str, config: Dict or None, name: str = None):
        self.type = type
        self.name = name or ""
        self.config = config or {}

        if not self.type:
            raise CrawlinoValueError("Config must has the 'type' property")

        if self.config is None:
            raise CrawlinoValueError("Source must has a 'config' property")

        if CrawlinoModulesStore.find_module(STEP_EXTRACTOR, self.type) is None:
            raise CrawlinoValueError(f"Invalid 'type' property value: "
                                     f"'{self.type}'",
                                     exc_info=True,
                                     extra={
                                         "input_type": self.type
                                     })

    @property
    def to_dict(self):
        return {
            "type": self.type,
            "config": self.config,
            "name": self.name
        }

    @property
    def module_name(self) -> str:
        return "extractors"


class CMRuleSet(metaclass=CModelBaseLoader):

    # __slots__ = ("type", "config", "name", "description")

    def __init__(self, config: dict):
        #
        # Mandatory args
        #
        for x in ("name", "mapTo", "inputVar"):
            try:
                setattr(self, un_camel(x), config[x])
            except KeyError:
                raise CrawlinoValueError(
                    f"Keyword '{x}' is necessary in the ruleSet definition")

        try:
            raw_rules = config["rules"]
        except KeyError:
            raise CrawlinoValueError(
                f"you must define at least one rule in a 'ruleSet' entry")
        else:
            self.rules = OrderedDict()
            for i, rule in enumerate(raw_rules):
                position = str(rule.get("config", {}).get("order", i))

                if position in self.rules.keys():
                    raise CrawlinoValueError(
                        f"conflict in order parameter for rules in ruleSet "
                        f"'{self.name}': already is an element with "
                        f"position '{position}'")

                self.rules[position] = CMRule(
                    type=rule.get("type"),
                    config=rule.get("config"),
                    name=rule.get("name")
                )

        #
        # Optional
        #
        self.description = config.get("description", "")
        self.exit_on_match = config.get("exitOnMatch", True)
        self.report = config.get("report", "group")

    def __iter__(self):
        self._iter_rules = self.rules.values().__iter__()
        return self

    def __next__(self):
        return next(self._iter_rules)


__all__ = ("CMRuleSet",)