from babelrts.components.dependencies.language import Language
from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction

class Swift(Language):

    def get_extensions_patterns_actions(self):
        return ()

    @staticmethod
    def get_language():
        return 'swift'