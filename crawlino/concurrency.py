import abc
import importlib
import logging

from typing import Dict, List
from multiprocessing import Queue, Process, Value

import time

from crawlino_core import STEP_HOOKS
from crawlino_core.modules_stores import CrawlinoModulesStore

from crawlino.current_config import current_config
from crawlino.models.plugins_models import PluginReturnedData

log = logging.getLogger("crawlino")


def execute(module_name: str,
            plugin_type: str,
            previous_step_result: PluginReturnedData or None,
            plugin_config: Dict):

    def _execute_plugin_():

        fn = CrawlinoModulesStore.find_module(module_name, plugin_type)

        log.debug(f"Executing plugin "
                  f"'{plugin_type}' - Parameters: {plugin_config}")

        #
        # Sources module runs the first, then the don't have any  previous
        # result from other step
        #
        return fn(previous_step_result, **plugin_config)

    ret = _execute_plugin_()

    return ret


class MultiTask:

    @abc.abstractclassmethod
    def join(self):
        pass

    @abc.abstractclassmethod
    def launch(self,
               crawler,
               previous_result,
               model,
               callback):
        pass

    def resolve_callback(self, name: str):
        if not name:
            return None

        return getattr(importlib.import_module(
                "crawlino.crawlino_managers.steps_executors"),
                name)


class MultiTaskProcesses(MultiTask):
    __pool__: List[Process] = None
    __queue__: Queue = Queue()
    __stoppable__: Value

    def __init__(self):
        if not MultiTaskProcesses.__pool__:
            MultiTaskProcesses.__pool__ = []
            MultiTaskProcesses.__stoppable__ = Value('i', 0)

            for _ in range(current_config.running_config.concurrency):
                c = Process(target=self._process_element,
                            args=(MultiTaskProcesses.__queue__,
                                  MultiTaskProcesses.__stoppable__)
                            )
                MultiTaskProcesses.__pool__.append(c)
                c.start()

    def _process_element(self, queue: Queue, stoppable: Value):
        while True:
            args = queue.get()

            crawler_name, current_step, plugin_type, \
                previous_results, config, callback = args

            ret = execute(*[
                current_step, plugin_type, previous_results, config
            ])

            #
            # Get function to call. We must get this way because
            # in this point of execution, the current process don't have
            # the context of loaded next function
            #
            if callback:
                fn = self.resolve_callback(callback)

                fn(ret, crawler_name)

            #
            # If we reached last execution step we set the working flow as a
            # "stoppable". The reason to do that is to avoid raise-conditions
            # when we start the execution of processes and when we need to
            # wait for the execution finish
            #
            if current_step == STEP_HOOKS:
                stoppable.value = 1

    def launch(self,
               crawler,
               previous_result,
               model,
               callback):

        for m in model:
            args = (crawler,
                    model.module_name,
                    model.type,
                    previous_result,
                    m,
                    callback)

            self.__queue__.put_nowait(args)

    def join(self):
        while True:
            if not MultiTaskProcesses.__queue__.empty() or \
                    not MultiTaskProcesses.__stoppable__.value:
                time.sleep(1)
            else:
                break

        for p in MultiTaskProcesses.__pool__:
            p.terminate()


class MultiTaskSequential(MultiTask):

    def launch(self,
               crawler,
               previous_result,
               model,
               callback):

        for m in model:
            r = execute(model.module_name,
                        model.type,
                        previous_result,
                        m)

            if callback:
                fn = self.resolve_callback(callback)

                fn(r, crawler)

    def join(self):
        pass


def map_concurrently(crawler_name: str,
                     previous_result,
                     model,
                     callback=None) -> MultiTask:

    c = None
    # -------------------------------------------------------------------------
    # Select concurrency method
    # -------------------------------------------------------------------------
    if current_config.running_config.concurrency_type == "processes":
        c = MultiTaskProcesses()
    elif current_config.running_config.concurrency_type == "sequential":
        c = MultiTaskSequential()

    # Launch tasks
    c.launch(crawler_name,
             previous_result,
             model,
             callback)

    return c

