from typing import List, Dict, Union

from crawlino_core import CrawlinoValueError, CrawlinoNotFoundError, \
    CrawlinoFormatError

from crawlino.helpers import gt
from crawlino.models.bases import CModelBase
from crawlino.mini_lang import detect_actions

ALLOWED_CONFIGURATION_FILES_FORMAT = (
    "json",
)
ALLOWED_TABLE_FIELD_TYPES = (
    "text",
    "datetime",
    "number",
    "boolean"
)


# --------------------------------------------------------------------------
# Fields
# --------------------------------------------------------------------------
class CMModelsField:
    def __init__(self,
                 name: str,
                 type: str,
                 key: bool = False):
        self.key = key
        self.type = type
        self.name = name


class CMModelsFields:

    def __init__(self, fields: List[Dict]):
        self._raw_data = fields
        self.fields = {}

        if not fields:
            return

        for field in fields:
            f = CMModelsField(field["name"],
                              field["name"],
                              gt(field, "key", False))

            if f.name in self.fields.keys():
                raise CrawlinoFormatError("Repeated property type for fields",
                                          exc_info=True,
                                          extra={
                                              'repeated_field': f.name
                                          })

            self.fields[f.name] = f

    def get(self, field_name: str) -> CMModelsField or CrawlinoNotFoundError:
        try:
            return self.fields[field_name]
        except KeyError:
            raise CrawlinoNotFoundError("Invalid field type",
                                        exc_info=True,
                                        extra={
                                            'requested_field': field_name
                                        })


# --------------------------------------------------------------------------
# Mappers
# --------------------------------------------------------------------------
class CMModelsMappersObject:
    pass


class CMModelsMappersDataGeneric(CMModelsMappersObject):

    def __init__(self, **kwargs):
        self.name = kwargs.get("type")


class CMModelsMappersDataBase(CMModelsMappersObject):

    def __init__(self,
                 name: str,
                 host: str,
                 port: str,
                 database: str,
                 collection: str,
                 user: str = None,
                 password: str = None):
        self.name = name
        self.port = port
        self.host = host
        self.database = database
        self.collection = collection

        self.user = user
        self.password = password


class CMModelsMappers:

    MAPPERS = {
        "database": CMModelsMappersDataBase,
        "raw": CMModelsMappersDataGeneric,
        "csv": CMModelsMappersDataGeneric,
        "stdout": CMModelsMappersDataGeneric
    }

    def __init__(self, fields: List[dict]):
        self._raw_data = fields

        self.mappers = {}

        for m in fields:
            # Get the key
            ks = list(m.keys())

            if len(ks) != 1:
                raise CrawlinoFormatError("Invalid mapper format. Each map, "
                                          "only can have one dictionary value",
                                          exc_info=True,
                                          extra={
                                              "map_value": str(m)
                                          })

            key_action = ks[0]

            # Determinate what sub-class build
            try:
                map_obj = self.MAPPERS[key_action](**m[key_action])
            except KeyError:
                raise CrawlinoValueError("Invalid mapper",
                                         exc_info=True,
                                         extra={
                                             "mapper_name": key_action
                                         })
            except TypeError as e:
                invalid_arg = e.args[0][e.args[0].rfind("argument") +
                                        len("argument"):]

                raise CrawlinoValueError("Invalid mapper. Mapper destination "
                                         "doesn't required property",
                                         exc_info=True,
                                         extra={
                                             "invalid_property": invalid_arg,
                                             "mapper_name": key_action
                                         })


            # Storage the object
            self.mappers[map_obj.name] = map_obj

    def all(self) -> List[CMModelsMappersObject]:
        return list(self.mappers.values())

    def get(self, mapper_name: str) -> CMModelsMappersObject:
        try:
            return self.mappers[mapper_name]
        except KeyError:
            raise CrawlinoNotFoundError("Mapper type not fount",
                                        exc_info=True,
                                        extra={
                                            "mapper_name": mapper_name
                                        })


class CMModel(CModelBase):

    def __init__(self, model: dict):

        # Load external
        if model:
            if isinstance(model, str):
                _model = detect_actions(model)

                if not model:
                    raise CrawlinoValueError("Invalid model input values",
                                             exc_info=True,
                                             extra={
                                                 "input_model": model
                                             })
                else:
                    model = _model

            # Inline declaration
            else:

                self.name = gt(model, "name", None)

                if not self.name:
                    raise CrawlinoValueError("Error in Models: Models must "
                                             "have 'type' property.")

                self.fields = CMModelsFields(gt(model, "fields", None))
                self.mappers = CMModelsMappers(gt(model, "mappers", None))


__all__ = ("CMModel", "CMModelsFields", "CMModelsMappers", "CMModelsField",
           "CMModelsMappersObject")
