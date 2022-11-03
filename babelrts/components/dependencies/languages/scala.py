from babelrts.components.dependencies.languages.java import Java
from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction

class Scala(Java):

    def get_extensions_patterns_actions(self):
        return self.get_token_extension_patterns_actions(('scala',),('import','new','extends'))

    @staticmethod
    def get_language():
        return 'scala'