from babelrts.components.dependencies.token_language import TokenLanguage

class Swift(TokenLanguage):

    def get_extensions(self):
        return 'swift'

    def get_tokens(self):
        return 'import'

    @staticmethod
    def get_language():
        return 'swift'