import abc

from crawlino_core.helpers import dict_to_object


class PluginReturned(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def to_dict(self) -> dict:
        pass


class PluginReturnedData(PluginReturned):

    def __init__(self, **kwargs):
        self._raw_values = {}
        for k, v in kwargs.items():
            setattr(self, k, v)
            self._raw_values[k] = v

    @property
    def to_dict(self):
        return {k: v
                for k, v in self.__dict__.items() if not k.startswith("_")}

    def json_property(self, json_name: str):
        """
        return a property accessing a a json format

        >>> data = {"hello": "world", "other": {"me": "two"}}
        >>> p = PluginReturnedData(**d)
        >>> p.json_property("hello")
        "world
        >>> p.json_property("other.me")
        "two"
        """
        try:
            #
            # Looking for specific attribute
            #
            prev = self._raw_values
            for attr in json_name.split("."):
                prev = prev[attr]

            return prev
        except KeyError:
            return None


__all__ = ("PluginReturnedData",)
