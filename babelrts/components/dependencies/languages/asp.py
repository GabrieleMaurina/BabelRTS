from babelrts.components.dependencies.token_language import TokenLanguage

class Asp(TokenLanguage):

    def get_extensions(self):
        return 'asp'

    def get_tokens(self):
        return '#include'

    @staticmethod
    def get_language():
        return 'asp'