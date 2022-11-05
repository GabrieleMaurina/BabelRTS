from babelrts.components.dependencies.token_language import TokenLanguage

class Php(TokenLanguage):

    def get_extensions(self):
        return 'php'

    def get_tokens(self):
        return ('include','require')

    @staticmethod
    def get_language():
        return 'php'