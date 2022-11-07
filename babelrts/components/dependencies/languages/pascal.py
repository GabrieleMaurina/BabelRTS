from babelrts.components.dependencies.token_language import TokenLanguage

class Pascal(TokenLanguage):

    def get_extensions(self):
        return 'p'

    def get_tokens(self):
        return 'uses'

    @staticmethod
    def get_language():
        return 'pascal'