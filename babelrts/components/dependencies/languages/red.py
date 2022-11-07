from babelrts.components.dependencies.token_language import TokenLanguage

class Red(TokenLanguage):

    def get_extensions(self):
        return 'red'

    def get_tokens(self):
        return 'load'

    @staticmethod
    def get_language():
        return 'red'