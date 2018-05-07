import os
import logging

from argparse import Namespace

from crawlino_core.crawlino_flow import STEP_SOURCES, STEP_CONFIG

from crawlino.crawlino import Crawlino
from crawlino.models import RunningConfig

from .common import CrawlinoManager
from .steps_executors import execute_config_step, execute_sources_step


log = logging.getLogger("crawlino")


# --------------------------------------------------------------------------
# Module runners
# --------------------------------------------------------------------------
class SimpleCrawlinoManager(CrawlinoManager):
    """
    This manager create Crawlino instances in a simple way. Load from
    a local path an launch it.

    This Manager works great for CLIs and scripting
    """

    def __init__(self, running_config: RunningConfig):
        super().__init__(running_config)

        # ---------------------------------------------------------------------
        # Load and configuration
        # ---------------------------------------------------------------------
        self.crawlers = {}
        self.running_config = running_config

        # ---------------------------------------------------------------------
        # Iter config
        # ---------------------------------------------------------------------
        self._step = 0

        # ---------------------------------------------------------------------
        # Update global config
        # ---------------------------------------------------------------------

    @classmethod
    def from_argparser(cls, argparser_input: Namespace):
        return SimpleCrawlinoManager(
            running_config=RunningConfig(
                paths=argparser_input.CRAWLERS_PATH,
                concurrency=argparser_input.concurrency,
                concurrency_type=argparser_input.concurrency_type,
                environment_vars=argparser_input.environment_vars,
                environment_file=argparser_input.environment_file
            )
        )

    def load(self):
        """Load crawlers from paths"""
        for crawler_path in self.running_config.paths:

            crawler_path_abs = os.path.abspath(crawler_path)

            if not os.path.isdir(crawler_path_abs):
                self.crawlers[crawler_path_abs] = Crawlino(
                    crawler_path_abs,
                    self.running_config
                )

            else:
                for root, dirs, files in os.walk(crawler_path_abs):
                    for f in files:
                        if any(f.startswith(x) for x
                               in ("crawlino", "crawler")) and \
                                any(f.endswith(x) for x
                                    in Crawlino.VALID_CRAWLER_EXTENSIONS):

                            # Load crawler
                            self.crawlers[f] = Crawlino(f,
                                                        self.running_config)

        # add to global config
        for c in self.crawlers.values():
            self.update_global_config(c)

        log.info(f"Loaded {len(self.crawlers)} crawlers")

    def run(self):

        # ---------------------------------------------------------------------
        # ---- METHOD STARTS HERE ----
        # ---------------------------------------------------------------------

        tasks = []
        # Run all crawlers
        for c_name, crawler_object in self.crawlers.items():
            log.info(f"Launching crawler '{c_name}'")
            for _ in crawler_object:

                current_module = crawler_object.current_module

                if current_module == STEP_CONFIG:
                    execute_config_step(crawler_object.name)

                elif current_module == STEP_SOURCES:
                    tasks.append(execute_sources_step(crawler_object.name))

                # After Input step, program flow are managed by Input step
                else:
                    continue

        for t in tasks:
            t.join()


__all__ = ("SimpleCrawlinoManager",)
