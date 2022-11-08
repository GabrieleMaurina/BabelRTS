from babelrts.components.dependencies.language import Language
from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction

from abc import abstractmethod
from re import compile as cmp_re
from os.path import basename, dirname

TOKEN_PATTERN = r'(?<!\S)(?:{})(.+)'
SPLIT_PATTERN = cmp_re(r'\W+')

class TokenLanguage(Language):

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
        dependencies = set()
        tokens = SPLIT_PATTERN.split(match)
        all_files = self.get_dependency_extractor().get_babelrts().get_change_discoverer().get_all_files()
        for token in tokens:
            token = token.lower()
            for file in all_files:
                name = basename(file).rsplit('.', 1)[0].lower()
                if name == token:
                    dependencies.add(file)
        if not dependencies:
            token = tokens[-1].lower()
            for file in all_files:
                folder = basename(dirname(file)).lower()
                if folder == token:
                    dependencies.add(file)
        return dependencies

    def get_pattern_for_tokens(self, tokens):
        return cmp_re(TOKEN_PATTERN.format('|'.join(tokens)))
