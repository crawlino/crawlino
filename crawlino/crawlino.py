from crawlino.models import CrawlinoModel, File, RunningConfig


def _build_runners_(model):
    return {
        "config": model.config,
        "sources": model.sources,
        "input": model.input,
        "extractors": model.extractors,
        # "model": model.model,
        "hooks": model.hooks
    }


class Crawlino:
    """
    This class store all information about a Crawler.

    Each class instance represent a different crawler
    """

    VALID_CRAWLER_EXTENSIONS = ("json", "yaml")

    def __init__(self,
                 file_definition: File or str,
                 running_config: RunningConfig = None):
        self.running_config = running_config or RunningConfig()
        self.definition_file = file_definition \
            if isinstance(file_definition, File) \
            else File(file_definition)

        self.model = CrawlinoModel(self.definition_file)

        # ---------------------------------------------------------------------
        # Map basic Crawler description
        # ---------------------------------------------------------------------
        self.name = self.model.name
        self.tags = self.model.tags
        self.description = self.model.description

        # Vars used for do Crawlino in iterable
        self._models_map_ = _build_runners_(self.model)
        self._models_map_positions_ = {
            name: pos
            for pos, name in enumerate(self._models_map_.keys())
        }
        self._step = self._models_map_.__iter__()
        self.current_module = None

    def __iter__(self):
        return self

    def __next__(self):
        self.current_module = mod_name = next(self._step)

        return self._models_map_[mod_name]

    def get_next_step(self, current_step: str):
        try:
            i = self._models_map_positions_[current_step] + 1
            next_item_name = list(self._models_map_.keys())[i]

            return self._models_map_[next_item_name]
        except (IndexError, KeyError):
            return None


__all__ = ("Crawlino",)
