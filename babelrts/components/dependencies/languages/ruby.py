from babelrts.components.dependencies.language import Language
from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction

class Ruby(Language):

    def get_extensions_patterns_actions(self):
        return self.get_token_extension_patterns_actions(('rb',),('load','require','include','extend','prepend', 'java_import', 'include_class', 'import'))

    @staticmethod
    def get_language():
        return 'ruby'