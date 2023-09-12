from babelrts.components.dependencies.languages.c import C
from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction

EXTENSIONS = ('h', 'cpp', 'hpp', 'cc')

class Cpp(C):

    def get_extensions_patterns_actions(self):
        c_extension_pattern_action = super().get_extensions_patterns_actions()
        return tuple(ExtensionPatternAction(extension, c.pattern, c.action) for extension in EXTENSIONS for c in c_extension_pattern_action)

    @staticmethod
    def get_language():
        return 'c++'