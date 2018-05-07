import os
import yaml
import glob
import logging
import os.path as op

from typing import List, Optional

try:
    import ujson as json
except ImportError:
    import json

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from crawlino_core import CrawlinoFormatError, CrawlinoValueError

log = logging.getLogger("crawlino")


class File:
    """Class that storage all information of a file"""

    def __init__(self, path: str, *, name: str = None, file_handler=None) -> \
            Optional[CrawlinoFormatError]:

        if not path:
            raise CrawlinoFormatError("Invalid file path",
                                      exc_info=True)

        self.path = path
        self.name = name or os.path.basename(path)
        self._handler = file_handler or open(self.path)
        self._file_type = None
        self._loaded_data = None

        # Load file data
        self.__load__()

    def __load__(self) -> Optional[CrawlinoFormatError]:
        """Detect the file type. Possible values are: json | yaml"""
        # Try to detect the file type trying to load as a JSON and YAML.
        # The reason y because we can not trust of the file extension
        try:
            self._loaded_data = json.load(self._handler)
            self._file_type = "json"
        except Exception:
            # Put the buffer at the beginning of the file. Because we already
            # try to open when we tried to as JSON
            self._handler.seek(0)

            # Try to load YAML
            try:
                self._loaded_data = yaml.load(self._handler, Loader=Loader)
                self._file_type = "yaml"
            except Exception:
                raise CrawlinoFormatError("Invalid file file. Format should "
                                          "be JSON or YAML",
                                          exc_info=True,
                                          extra={
                                              "file_name": self.path
                                          })

    @property
    def file_type(self) -> str:
        return self._file_type

    @property
    def parsed(self) -> dict:
        """Return the file content and parsed it, depending of the file type
        the loaded information would be JSON data or YAML data."""
        return self._loaded_data


class RunningConfig:
    """This class stores the Crawlino configuration for run"""

    CONCURRENCY_MODES = ("processes", "sequential")

    def __init__(self,
                 paths: str or List[str],
                 default_crawler_extension: str = "yaml",
                 concurrency: int = 1,
                 concurrency_type: str = "threads",
                 environment_vars: List[str] = None,
                 environment_file: str = None,
                 crawlers_templates_path: List[str] or None = None):
        if not default_crawler_extension:
            self.default_crawler_extension: str = "yaml"
        else:
            self.default_crawler_extension: str = default_crawler_extension

        # ---------------------------------------------------------------------
        # Paths
        # ---------------------------------------------------------------------
        if isinstance(paths, list):
            tmp_paths = paths
        else:
            tmp_paths = [paths if paths else ""]

        # Expand any Glob in paths: *.py -> 1.py, 2.py...
        self.paths = [op.abspath(e) for x in tmp_paths for e in glob.glob(x)]

        try:
            con = int(concurrency)
        except ValueError:
            con = 1
        self.concurrency: int = 1 if con < 1 else con

        if concurrency_type not in self.CONCURRENCY_MODES:
            raise CrawlinoValueError(f"Invalid concurrency type. Allowed types"
                                     f" are: "
                                     f"{'|'.join(self.CONCURRENCY_MODES)}")

        self.concurrency_type = concurrency_type

        self.crawlers_templates_path = [
            op.abspath(op.join(op.dirname(__file__),
                               "..",
                               "crawlers_templates"))
        ]

        if crawlers_templates_path:
            if not isinstance(crawlers_templates_path, list):
                crawlers_templates_path = [crawlers_templates_path]

            self.crawlers_templates_path.extend(crawlers_templates_path)

        # ---------------------------------------------------------------------
        # Set environment vars
        # ---------------------------------------------------------------------
        self.environment_vars = []

        self.environment_file = environment_file
        if self.environment_file:
            self.environment_file = op.abspath(environment_file)

            with open(self.environment_file, "r") as f:
                self.environment_vars.extend(f.read().splitlines())

        if environment_vars:
            self.environment_vars.extend(environment_vars)

        # Remove duplicates
        self.environment_vars = list(set(self.environment_vars))

        if self.environment_vars:
            for v in self.environment_vars:
                if "=" not in v:
                    raise CrawlinoFormatError(
                        f"Environment vars must be set as format: VAR=VALUE. "
                        f"Got: '{v}'")

                try:
                    var_name, var_value = v.split("=")
                except ValueError:
                    raise CrawlinoFormatError(
                        f"Environment vars must be set as format: VAR=VALUE. "
                        f"Got: '{v}'")

                log.debug(f"Setting environment var '{var_name}' with value "
                          f"'{var_value}'")

                os.environ[var_name] = var_value

        log.info(f"Working mode '{self.concurrency_type}' with "
                 f"concurrency '{self.concurrency}'")

        log.info(f"Selected {len(self.crawlers_templates_path)} "
                 f"crawlers paths")
        log.info(f"Default crawler extension selected: "
                 f"'{self.default_crawler_extension}")


__all__ = ("File", "RunningConfig")
