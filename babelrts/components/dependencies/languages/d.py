from babelrts.components.dependencies.token_language import TokenLanguage

class D(TokenLanguage):

    def get_extensions(self):
        return 'd'

    def get_tokens(self):
        return 'import'

    @staticmethod
    def get_language():
        return 'd'