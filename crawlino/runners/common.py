import abc

from crawlino.models import RunningConfig
from crawlino.current_config import current_config


class CrawlinoManager(metaclass=abc.ABCMeta):
    """
    Abstract class for run managers

    This class also manages the app config contexts
    """

    def __init__(self, running_config: RunningConfig):
        current_config.running_config = running_config

    def update_global_config(self, crawler):
        current_config.add_crawler_crawler(crawler)

