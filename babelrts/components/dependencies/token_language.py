from babelrts.components.dependencies.language import Language
from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction

from abc import abstractmethod
from re import compile as cmp_re
from os.path import basename

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
        for token in SPLIT_PATTERN.split(match):
            token = token.lower()
            for file in self.get_dependency_extractor().get_babelrts().get_change_discoverer().get_all_files():
                name = basename(file).rsplit('.', 1)[0].lower()
                if name == token:
                    dependencies.add(file)
        return dependencies

    def get_pattern_for_tokens(self, tokens):
        return cmp_re(TOKEN_PATTERN.format('|'.join(tokens)))
