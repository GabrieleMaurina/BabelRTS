from babelrts.components.dependencies.language import Language
from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction

from re import compile as cmp_re
from os.path import basename

IMPORT_PATTERN = cmp_re(r'(?<!\S)-import\s*\(\s*(\S+?)\s*,')
INCLUDE_PATTERN = cmp_re(r'(?<!\S)-include(?:_lib)?\s*\(\s*"(\S+?)"\s*\)')
CALL_PATTERN = cmp_re(r'(\w+):\w+\(')

class Erlang(Language):

    def get_extensions_patterns_actions(self):
        return (
            ExtensionPatternAction('erl', IMPORT_PATTERN, self.module_action),
            ExtensionPatternAction('hrl', IMPORT_PATTERN, self.module_action),
            ExtensionPatternAction('erl', CALL_PATTERN, self.module_action),
            ExtensionPatternAction('hrl', CALL_PATTERN, self.module_action),
            ExtensionPatternAction('erl', INCLUDE_PATTERN, self.include_action),
            ExtensionPatternAction('hrl', INCLUDE_PATTERN, self.include_action)
        )

    @staticmethod
    def get_language():
        return 'erlang'

    def module_action(self, match, file_path, folder_path, content):
        dependencies = set()
        for file in self.get_dependency_extractor().get_babelrts().get_change_discoverer().get_all_files():
            name = basename(file).rsplit('.', 1)[0]
            if name == match:
                dependencies.add(file)
        return dependencies

    def include_action(self, match, file_path, folder_path, content):
        return self.module_action(basename(match).rsplit('.', 1)[0], file_path, folder_path, content)