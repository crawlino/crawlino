from typing import Dict

from crawlino_core import CrawlinoValueError
from crawlino_core.modules_stores import CrawlinoModulesStore

from crawlino.models import CModelBase, CModelBaseLoader


class CMHook(CModelBase, metaclass=CModelBaseLoader):

    __slots__ = ("type", "config", "name")

    def __init__(self, type: str, config: Dict or None, name: str = None):
        self.type = type
        self.name = name or ""
        self.config = config or {}

        if CrawlinoModulesStore.find_module("hooks", self.type) is None:
            raise CrawlinoValueError("Invalid 'type' property value",
                                     exc_info=True,
                                     extra={
                                         "given_source_type": self.type
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
    def module_name(self) -> str:
        return "hooks"


__all__ = ("CMHook", )
