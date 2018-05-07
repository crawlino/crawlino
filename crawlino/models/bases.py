import abc

from crawlino_core import CrawlinoException
from crawlino.helpers import GeneratorDiscover
from crawlino.mini_lang import do_import, do_replacer_vars


class CModelBaseLoader(type):

    def __call__(cls, *args, **kwargs):
        # Has "type" property an $import
        input_return_type = do_import(kwargs.get("type"))
        input_return_config = do_import(kwargs.get("config"))

        # If dict -> has an import
        if isinstance(input_return_type, dict):

            # If import is in "type" then is a complete import
            kwargs["name"] = input_return_type.get("name", "")

            try:
                kwargs["type"] = input_return_type["type"]
            except KeyError:
                raise CrawlinoException("Imported value must have 'type' "
                                        "keyword")

            try:
                kwargs["config"] = input_return_type["config"]
            except KeyError:
                raise CrawlinoException("Imported value must have 'config' "
                                        "keyword")

        elif not isinstance(kwargs.get("config", None), dict) and \
                isinstance(input_return_config, dict):
            try:
                kwargs["config"] = input_return_config["config"]
            except KeyError:
                raise CrawlinoException("Imported value must have 'config' "
                                        "keyword")

        instance = super(CModelBaseLoader, cls).__call__(*args, **kwargs)

        return instance


class CModelBase:

    @property
    @abc.abstractclassmethod
    def to_dict(self) -> dict:
        pass

    @property
    @abc.abstractclassmethod
    def module_name(self) -> str:
        pass

    def __iter__(self):
        self.gg = GeneratorDiscover(self.to_dict).__iter__()
        return self

    def __next__(self):
        return next(self.gg)

    def __setattr__(self, key, value):

        def _convert(item, current: str = None):
            """This function try to find environment vars"""
            if isinstance(item, dict):
                try:
                    return {
                        k: _convert(
                            v,
                            f"{current}.{k}" if current else k
                        )
                        for k, v in item.items()
                    }
                except ValueError:
                    pass
            if isinstance(item, list):
                #
                # Currently List are not permitted
                #
                return [
                    _convert(v, f"{current}.{k}") if current else k
                    for k, v in enumerate(item)
                ]

            else:
                return do_replacer_vars(str(item))

        if value and isinstance(value,
                                (list, dict, tuple, int, float, str, set)):
            converted_value = _convert(value)
        else:
            converted_value = value

        super().__setattr__(key, converted_value)


__all__ = ("CModelBase", "CModelBaseLoader")
