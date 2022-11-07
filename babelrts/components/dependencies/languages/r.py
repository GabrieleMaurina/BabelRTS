from babelrts.components.dependencies.token_language import TokenLanguage

class R(TokenLanguage):

    def get_extensions(self):
        return 'R'

    def get_tokens(self):
        return ('source','library','require','use')

    @staticmethod
    def get_language():
        return 'r'