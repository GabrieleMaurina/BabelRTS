from babelrts.components.dependencies.token_language import TokenLanguage

class Haskell(TokenLanguage):

    def get_extensions(self):
        return 'hs'

    def get_tokens(self):
        return 'import'

    @staticmethod
    def get_language():
        return 'haskell'