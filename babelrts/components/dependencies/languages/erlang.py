from babelrts.components.dependencies.language import Language
from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction

from re import compile as cmp_re

IMPORT_PATTERN = cmp_re(r'(?<!\S)-import\s*\(\s*(\S+?)\s*,')
CALL_PATTERN = cmp_re(r'(\w+):\w+\(')

class Erlang(Language):

    def get_extensions_patterns_actions(self):
        return (
            ExtensionPatternAction('erl', IMPORT_PATTERN, self.import_action),
            ExtensionPatternAction('hrl', IMPORT_PATTERN, self.import_action),
            ExtensionPatternAction('erl', CALL_PATTERN, self.call_action),
            ExtensionPatternAction('hrl', CALL_PATTERN, self.call_action)
        )

    @staticmethod
    def get_language():
        return 'erlang'

    def import_action(self, match, file_path, folder_path, content):
        pass

    def call_action(self, match, file_path, folder_path, content):
        pass