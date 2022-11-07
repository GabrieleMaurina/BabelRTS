from babelrts.components.dependencies.token_language import TokenLanguage

class StandardML(TokenLanguage):

    def get_extensions(self):
        return 'sml'

    def get_tokens(self):
        return 'use'

    @staticmethod
    def get_language():
        return 'standardml'