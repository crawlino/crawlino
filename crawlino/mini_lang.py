import re
import os.path as op

from typing import Callable, List, Tuple, Any

import os

from crawlino_core.helpers import find_file
from crawlino_core.exceptions import CrawlinoNotFoundError, CrawlinoValueError

#
# def import_action(source_file_name: str, *config_files):
#
#     for l in config_files:
#
#         # Try to resolve loader
#         file_name = l if ".json" in l else f"{l}.json"
#
#         # Get path
#         file_name = op.join(op.dirname(source_file_name),
#                             file_name)
#
#         # Find file
#         location = find_file(file_name)
#
#         return json.load(open(location))
#
#
# MODEL_FUNCTION_MAPPING = {
#     'import': import_action
# }

ACTIONS_DETECTION_REGEX = re.compile(
        r'''(\$)([\w\d]+)([\(\s\"\'\/]+)([\w\'_\"\-\.\d\/\, ]+)([\)\s]+)''')

VARS_DETECTION_REGEX = re.compile(
    r'''(\$)([\w\_\-\.]+)(\$)'''
)

# def old_detect_actions(text: str) -> Tuple[Callable, List] or None:
#     tokenized = tokenize(io.BytesIO(text.encode("utf-8")).readline)
#
#     found_fn = None
#     record_function = False
#     record_parameters = True
#     fn_parameters = []
#
#     for token in tokenized:
#         if token.type == 53:  # OP
#
#             if token.string == "$":
#                 record_function = True
#
#             elif token.string == "(":
#                 record_function = False
#                 record_parameters = True
#             elif token.string == ")":
#                 record_parameters = False
#
#         elif token.type == 1 and record_parameters and \
#                 record_function is False:  # NAME
#             fn_parameters.append(text[token.start[1]: token.end[1]])
#
#         elif token.type == 1 and record_function:  # Params
#             found_fn = text[token.start[1]: token.end[1]]
#
#     return found_fn, fn_parameters


def detect_actions(text: str) -> List[Tuple[Callable, List]] or None:
    try:
        action_found = ACTIONS_DETECTION_REGEX.findall(text)
    except TypeError:
        return None

    if not action_found:
        return None

    else:
        results = []
        for _, fn, _, raw_fn_args, _ in action_found:
            fn_args = []
            for x in raw_fn_args.split(","):
                # Detect each parameter type
                _x = x.strip()
                try:
                    v = int(_x)
                except ValueError:
                    try:
                        v = float(_x)
                    except ValueError:
                        v = _x.replace("'", "").replace('"', '')

                fn_args.append(v)

            results.append((fn, fn_args))

        return results


def do_replacer_vars(text: str) -> str:
    if not text:
        return text

    i = 0
    results = []
    iter_text = text
    while True:
        try:
            found = VARS_DETECTION_REGEX.search(iter_text)
        except TypeError:
            return text

        # Replace generator results with generated data
        if found:
            var_name = found.group(2)
            try:
                env_var_value = os.environ[var_name]
            except KeyError:
                raise CrawlinoValueError(
                    f"Can't find environment var '{var_name}'. Can't replace"
                    f" '${var_name}$' in the crawler")

            start, end = found.span()
            results.extend(
                [
                    iter_text[:start],
                    env_var_value
                ]
            )
            iter_text = iter_text[end:]
            i += 1
        else:
            if iter_text:
                results.append(iter_text)

            break

    return "".join(results)


def do_import(text: str) -> dict or str:
    """
    This function try to import an external module and return a dict

    >>> do_import("$import(sources/mySource.yml)")
    {
        "type": "domain",
        "config" : {}
    }

    Also can import partial parts

    >>> do_import("$import(sources/mySourceConfig.yml)")
    {
        "config" : {}
    }

    If there is nothing to import, return the original object
    """
    from crawlino.current_config import current_config

    something_action = detect_actions(text)

    if not something_action:
        return text

    for action in something_action:

        try:
            action_name, action_params = action

            if action_name != "import":
                continue

            if len(action_params) != 1:
                raise CrawlinoValueError("Import function must "
                                         "has only 1 parameters")

        except ValueError:
            raise CrawlinoValueError(
                f"Format error for input function. Valid format is: "
                f"$import(source/myModule)")

        # Load file
        here = os.getcwd()

        if "/" in action_params[0]:
            part_type, part_name = action_params[0].split("/")
        else:
            part_type = None
            part_name = action_params[0]

        # Search for part
        loaded_data = None
        parts_folders = current_config.running_config.crawlers_templates_path
        for part_folder in parts_folders:
            for root, dirs, files in os.walk(part_folder):
                for f in files:

                    # Check that import type.
                    # sources/sample -> only load sources types
                    if part_type and not root.endswith(part_type):
                        continue

                    f_name, f_extension = op.splitext(f)

                    if f_name != part_name:
                        continue

                    if f_extension == ".json":
                        import json
                        loaded_data = json.load(open(
                                op.join(root, f),
                                "r"
                            ))
                    elif any(f_extension == x for x in (".yaml", ".yml")):
                        import yaml

                        loaded_data = yaml.safe_load(
                            open(
                                op.join(root, f),
                                "r"
                            )
                        )

                    if loaded_data:
                        break

        return loaded_data


def do_script(obj: str or Any, source_file_name: str = None):
    if type(obj) is str and obj:
        action, args = detect_actions(obj)

        if not action:
            return obj

        # Finding action in map
        try:
            fn = MODEL_FUNCTION_MAPPING[action]
        except KeyError:
            raise CrawlinoNotFoundError("Invalid script action",
                                        exc_info=True,
                                        extra={
                                            "invalid_action": action
                                        })

        # Call the function
        return fn(source_file_name,
                  *args)

    else:
        return obj


__all__ = ("detect_actions", "do_script", "do_import", "do_replacer_vars")
