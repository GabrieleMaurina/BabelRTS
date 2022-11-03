from babelrts.components.dependencies.language import Language
from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction

class Groovy(Language):

    def get_extensions_patterns_actions(self):
        return self.get_token_extension_patterns_actions(('groovy', 'gvy', 'gy', 'gsh'),('import','extends','implements','new'))

    @staticmethod
    def get_language():
        return 'groovy'