from babelrts.components.dependencies.languages.c import C
from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction

class Cpp(C):

    def get_extensions_patterns_actions(self):
        return (
            ExtensionPatternAction('h', INCLUDE_PATTERN, self.include_action),
            ExtensionPatternAction('cpp', INCLUDE_PATTERN, self.include_action),
            ExtensionPatternAction('hpp', INCLUDE_PATTERN, self.include_action),
            ExtensionPatternAction('cc', INCLUDE_PATTERN, self.include_action)
        )

    @staticmethod
    def get_language():
        return 'c++'