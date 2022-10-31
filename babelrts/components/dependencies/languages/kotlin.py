from babelrts.components.dependencies.languages.java import Java
from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction

class Kotlin(Java):

    def get_extensions_patterns_actions(self):
        return ()

    @staticmethod
    def get_language():
        return 'kotlin'