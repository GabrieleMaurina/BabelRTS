from babelrts.components.dependencies.token_language import TokenLanguage

class Pearl(TokenLanguage):

    def get_extensions(self):
        return 'pl'

    def get_tokens(self):
        return ('require','use')

    @staticmethod
    def get_language():
        return 'pearl'