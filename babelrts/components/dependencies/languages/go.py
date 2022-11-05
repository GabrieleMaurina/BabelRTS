from babelrts.components.dependencies.token_language import TokenLanguage

class Go(TokenLanguage):

    def get_extensions(self):
        return 'go'

    def get_tokens(self):
        return 'import'

    @staticmethod
    def get_language():
        return 'go'