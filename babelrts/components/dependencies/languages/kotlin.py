from babelrts.components.dependencies.token_language import TokenLanguage

class Kotlin(TokenLanguage):

    def get_extensions(self):
        return 'kt'

    def get_tokens(self):
        return 'import'

    @staticmethod
    def get_language():
        return 'kotlin'