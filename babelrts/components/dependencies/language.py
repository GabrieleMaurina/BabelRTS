from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction

from abc import ABC, abstractmethod
from os.path import join, isfile, isdir
from glob import glob
from re import compile as cmp_re

TOKEN_PATTERN = '(?<!\S)(?:{})(.+)'
SPLIT_PATTERN = cmp_re(r'\W+')

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

    def get_token_extension_patterns_actions(self, extensions, tokens):
        return tuple(ExtensionPatternAction(extension, self.get_pattern_for_tokens(tokens), self.token_action) for extension in extensions)

    def token_action(self, match, file_path, folder_path, content):
        dependencies = set()
        for token in SPLIT_PATTERN.split(match):
            token = token.lower()
            for file in self.get_dependency_extractor().get_babelrts().get_change_discoverer().get_all_files():
                name = basename(file).rsplit('.', 1)[0].lower()
                if name == token:
                    dependencies.add(file)
        return dependencies

    def get_pattern_for_tokens(self, tokens):
        return cmp_re(TOKEN_PATTERN.format('|'.join(tokens)))

    def get_additional_dependencies(self):
        return None

    def get_project_folder(self):
        return self.get_dependency_extractor().get_babelrts().get_project_folder()

    def get_dependency_extractor(self):
        return self._dependency_extractor

    def set_dependency_extractor(self, dependency_extractor):
        self._dependency_extractor = dependency_extractor