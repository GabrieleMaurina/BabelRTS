from babelrts.components.dependencies.token_language import TokenLanguage

class Cobra(TokenLanguage):

    def get_extensions(self):
        return 'cobra'

    def get_tokens(self):
        return 'use'

    @staticmethod
    def get_language():
        return 'cobra'