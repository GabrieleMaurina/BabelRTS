from babelrts.components.dependencies.language import Language
from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction

from abc import abstractmethod
from re import compile as cmp_re
from os.path import basename, dirname

TOKEN_PATTERN = r'(?<!\S)(?:{})(.+)'
SPLIT_PATTERN = cmp_re(r'\W+')

class TokenLanguage(Language):

    def __init__(self, dependency_extractor):
        super().__init__(dependency_extractor)
        self.reset()

    @abstractmethod
    def get_extensions(self):
        pass

    @abstractmethod
    def get_tokens(self):
        pass

    def get_extensions_patterns_actions(self):
        return self.get_token_extensions_patterns_actions(self.get_extensions(),self.get_tokens())

    def get_token_extensions_patterns_actions(self, extensions, tokens):
        if isinstance(extensions, str):
            extensions = (extensions,)
        if isinstance(tokens, str):
            tokens = (tokens,)
        return tuple(ExtensionPatternAction(extension, self.get_pattern_for_tokens(tokens), self.token_action) for extension in extensions)

    def token_action(self, match, file_path, folder_path, content):
        self.create_token_cache()
        dependencies = set()
        tokens = SPLIT_PATTERN.split(match)
        all_files = self.get_dependency_extractor().get_babelrts().get_change_discoverer().get_all_files()
        for token in tokens:
            token = token.lower()
            for file in self._file_tokens.get(token, ()):
                dependencies.add(file)
        if not dependencies:
            token = tokens[-1].lower()
            for file in self._folder_tokens.get(token, ()):
                dependencies.add(file)
        return dependencies

    def get_pattern_for_tokens(self, tokens):
        return cmp_re(TOKEN_PATTERN.format('|'.join(tokens)))

    def reset(self):
        self._file_tokens = {}
        self._folder_tokens = {}

    def create_token_cache(self):
        if not self._file_tokens:
            all_files = self.get_dependency_extractor().get_babelrts().get_change_discoverer().get_all_files()
            for file in all_files:
                name = basename(file).rsplit('.', 1)[0].lower()
                folder = basename(dirname(file)).lower()

                if name not in self._file_tokens: self._file_tokens[name] = []
                self._file_tokens[name].append(file)

                if folder not in self._folder_tokens: self._folder_tokens[folder] = []
                self._folder_tokens[folder].append(file)

    def get_additional_dependencies(self):
        self.reset()
