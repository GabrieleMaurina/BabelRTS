from babelrts.components.dependencies.languages.c import C
from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction

class Cpp(C):

    def get_extensions_patterns_actions(self):
        return ()

    @staticmethod
    def get_language():
        return 'c++'