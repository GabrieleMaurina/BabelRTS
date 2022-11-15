from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction

from abc import ABC, abstractmethod
from os.path import join, isfile, isdir, relpath, normpath
from glob import glob
from itertools import chain

class Language(ABC):

    def __init__(self, dependency_extractor):
        self._dependency_extractor = dependency_extractor

    def is_file(self, path):
        return isfile(join(self.get_project_folder(), normpath(path)))

    def is_dir(self, path):
        return isdir(join(self.get_project_folder(), normpath(path)))

    def expand(self, path):
        project_folder = self.get_project_folder()
        for value in glob(join(project_folder, normpath(path))):
            yield relpath(value, project_folder)

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

    def get_folders(self, folders=()):
        babelrts = self.get_dependency_extractor().get_babelrts()
        project_folder = babelrts.get_project_folder()
        source_folders = babelrts.get_source_folders()
        test_folders = babelrts.get_test_folders()
        if isinstance(folders, str):
            folders = (folders,)
        return chain((project_folder,), source_folders, test_folders, folders)

    def get_dependency_extractor(self):
        return self._dependency_extractor

    def set_dependency_extractor(self, dependency_extractor):
        self._dependency_extractor = dependency_extractor