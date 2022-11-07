from babelrts.components.dependencies.token_language import TokenLanguage

class Dart(TokenLanguage):

    def get_extensions(self):
        return 'dart'

    def get_tokens(self):
        return 'import'

    @staticmethod
    def get_language():
        return 'dart'