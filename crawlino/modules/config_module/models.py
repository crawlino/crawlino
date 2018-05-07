from typing import Dict

from crawlino_core.crawlino_flow import STEP_CONFIG
from crawlino_core.exceptions import CrawlinoValueError
from crawlino_core.modules_stores import CrawlinoModulesStore

from crawlino.models import CModelBase, CModelBaseLoader


class CMConfig(CModelBase, metaclass=CModelBaseLoader):

    __slots__ = ("type", "config", "name")

    def __init__(self, type: str, config: Dict or None, name: str = None):
        self.type = type
        self.name = name or ""
        self.config = config or {}

        if not self.type:
            raise CrawlinoValueError("Config must has the 'type' property")

        if self.config is None:
            raise CrawlinoValueError("Source must has a 'config' property")

        if CrawlinoModulesStore.find_module(STEP_CONFIG, self.type) is None:
            raise CrawlinoValueError("Invalid 'type' property value",
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
        return "config"


__all__ = ("CMConfig",)
