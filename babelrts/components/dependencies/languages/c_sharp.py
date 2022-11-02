from babelrts.components.dependencies.language import Language
from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction

from re import compile as cmp_re

NAMESPACE_PATTERN = cmp_re(r'(?<!\S)namespace\s+(\S+?)\s*[{;]')
USING_PATTERN = cmp_re(r'(?<!\S)using\s+(\S+?)\s*{')

class CSharp(Language):

    def get_extensions_patterns_actions(self):
        return  (
            ExtensionPatternAction('cs', NAMESPACE_PATTERN, self.namespace_action),
            ExtensionPatternAction('cs', USING_PATTERN, self.using_action)
        )

    @staticmethod
    def get_language():
        return 'c#'

    def namespace_action(self, match, file_path, folder_path, content):
        pass

    def using_action(self, match, file_path, folder_path, content):
        pass

    def get_additional_dependencies(self):
        return None