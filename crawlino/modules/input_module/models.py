from typing import Dict

from crawlino_core.exceptions import CrawlinoValueError
from crawlino_core.crawlino_flow import STEP_INPUT
from crawlino_core.modules_stores import CrawlinoModulesStore

from crawlino.models import CModelBase, CModelBaseLoader


class CMInput(CModelBase, metaclass=CModelBaseLoader):

    __slots__ = ("type", "config", "name")

    def __init__(self, type: str, config: Dict or None, name: str = None):
        self.type = type
        self.name = name or ""
        self.config = config or {}

        if not self.type:
            raise CrawlinoValueError("Input must has the 'type' property")

        if CrawlinoModulesStore.find_module(STEP_INPUT, self.type) is None:
            raise CrawlinoValueError("Invalid 'type' property value",
                                     exc_info=True,
                                     extra={
                                         "input_type": self.type
                                     })

        if self.config is None:
            raise CrawlinoValueError("Input must has a 'config' property")

    @property
    def to_dict(self):
        return {
            "type": self.type,
            "config": self.config,
            "name": self.name
        }

    @property
    def module_name(self):
        return "input"


__all__ = ("CMInput",)
