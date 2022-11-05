from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction

from abc import ABC, abstractmethod
from os.path import join, isfile, isdir
from glob import glob

class Language(ABC):

    def __init__(self, dependency_extractor):
        self._dependency_extractor = dependency_extractor

    def is_file(self, path):
        return isfile(join(self.get_project_folder(), path))

    def is_dir(self, path):
        return isdir(join(self.get_project_folder(), path))
        
    def expand(self, path):
        for value in glob(join(self.get_project_folder(), path)):
            yield value

    @abstractmethod
    def get_extensions_patterns_actions(self):
        pass

    @staticmethod
    @abstractmethod
    def get_language():
        pass

    def get_additional_dependencies(self):
        return None

    def get_project_folder(self):
        return self.get_dependency_extractor().get_babelrts().get_project_folder()

    def get_dependency_extractor(self):
        return self._dependency_extractor

    def set_dependency_extractor(self, dependency_extractor):
        self._dependency_extractor = dependency_extractor