import re

from itertools import product
from collections import defaultdict
from typing import Callable, Dict, List


# --------------------------------------------------------------------------
# Map the function to do code shorter
# --------------------------------------------------------------------------
from crawlino_core.modules_stores import CrawlinoModulesStore

ACTIONS_DETECTION_REGEX = \
    re.compile(r'''(\$)([\w\d\_\-]+)([\(\s]+)([\w\'_\"\-\.\d\, ]+)([\)\s]+)''')


def gt(obj, key, default):
    if isinstance(obj, dict):
        return obj.get(key, default)
    else:
        return obj


class GeneratorDiscover:
    """
    This class stores dictionaries and discover Crawlino generator defined in
    the strings of the values of them. Also allow:
    - discover total of generators defined
    - number of loop needed to generate all of the generators combinations
    - yield the generated combinations of generated data

    >>> data = {"name": "John Smith", "hometown": "/users/user?id=$generator('numeric', 1, 10)"}
    >>> g = GeneratorBuilder(data)
    >>> g.total_generators
    1
    >>> g.discovered_generators
    ["numeric"]
    >>> g.keys_with_generators
    {"hometown": ["numeric"]}
    >>> next(g)
    {"name": "John Smith", "hometown": "/users/user?id=1"}
    >>> next(g)
    {"name": "John Smith", "hometown": "/users/user?id=2"}
    """

    def __init__(self, data: Dict):
        self.raw_data: Dict = data
        self.generators = defaultdict(list)

        self._discovered_generators = None
        self._total_generators = None
        self._keys_with_generators = None

        self.map_keys_and_generators = {}

        # Parse
        self._locate_generators(self.raw_data)
        self._next_data = self._generate_data(self.raw_data)

    @property
    def discovered_generators(self) -> List[str]:
        if not self._discovered_generators:
            self._discovered_generators = list({
                fn
                for _, generators in self.generators.items()
                for fn, _ in generators
            })
        return self._discovered_generators

    @property
    def keys_with_generators(self) -> Dict[str, List[str]]:
        if not self._keys_with_generators:
            tmp = defaultdict(list)
            for key, generators in self.generators.items():
                for fn, fn_args in generators:
                    tmp[key].append((fn, fn_args))

            self._keys_with_generators = dict(tmp)

        return self._keys_with_generators

    @property
    def total_generators(self) -> int:
        if not self._total_generators:
            self._total_generators = sum([
                1
                for _, generators in self.generators.items()
                for _, _ in generators
            ])

        return self._total_generators

    def _generate_all_values(self):
        result = {}

        keys = list(self.map_keys_and_generators.keys())
        d = list(self.map_keys_and_generators.values())
        for x in product(*d):
            for i, v in enumerate(x):
                result[keys[i]] = v

            yield result

    def _locate_generators(self, item: Dict):
        """This function convert a Python Dict into a Python object:

        >>> data = {"name": "John Smith", "hometown": {"name": "New York",
        "id": 123}}type >>> c = json_to_object(data)
        >>> lambda d: d if not isinstance(d, int) else d * d
        >>>
        """
        from crawlino.mini_lang import detect_actions

        gen = self.generators
        map_keys_and_generators = self.map_keys_and_generators

        def convert(item, current: str = None):
            if isinstance(item, dict):
                return {
                    k: convert(
                        v,
                        f"{current}.{k}" if current else k
                    )
                    for k, v in item.items()
                }
            if isinstance(item, list):
                #
                # Currently List are not permitted
                #
                return [
                    convert(v, f"{current}.{k}") if current else k
                    for k, v in enumerate(item)
                ]

            else:
                # _item = str(item)
                _item = item
                if "$generator" in _item:
                    for i, (action, action_params) in \
                            enumerate(detect_actions(_item)):

                        # Set generator name
                        generator_name = action_params[0]
                        generator_params = action_params[1:]

                        gen[current].append(
                            (
                                generator_name,
                                generator_params
                            )
                        )

                        # Map current property with their generators
                        map_keys_and_generators[f"{current}_{i}"] = \
                            CrawlinoModulesStore.find_module(
                                "generators", generator_name
                            )(*generator_params)

        convert(item)

    def _generate_data(self, data) -> Dict:
        pre_generated_values = None

        def _data_generator(item, current: str = None):

            if isinstance(item, dict):
                res = {}
                for k, v in item.items():
                    res[k] = _data_generator(
                        v,
                        f"{current}.{k}" if current else k
                    )

                return res

            if isinstance(item, list):
                #
                # Currently List are not permitted
                #
                return [
                    _data_generator(v, f"{current}.{k}") if current else k
                    for k, v in enumerate(item)
                ]
            else:
                _item = str(item)
                if "$generator" not in _item:
                    return item
                else:
                    try:
                        results_text = []
                        i = 0
                        iter_text = _item
                        while True:
                            found = ACTIONS_DETECTION_REGEX.search(iter_text)

                            # Replace generator results with generated data
                            if found:
                                start, end = found.span()
                                curr_item = f"{current}_{i}"
                                value = pre_generated_values[curr_item]

                                results_text.extend(
                                    [
                                        iter_text[:start],
                                        str(value)
                                    ]
                                )
                                iter_text = iter_text[end:]
                                i += 1
                            else:
                                if iter_text:
                                    results_text.append(iter_text)

                                break

                        return "".join(results_text).strip()
                    except KeyError:
                        return item

        for d in self._generate_all_values():
            pre_generated_values = d
            yield _data_generator(data)

    def __iter__(self):
        return self

    def __next__(self) -> Dict:
        return next(self._next_data)


__all__ = ("gt", "GeneratorDiscover")
