from babelrts.components.dependencies.token_language import TokenLanguage

class MatLab(TokenLanguage):

    def get_extensions(self):
        return 'm'

    def get_tokens(self):
        return ('addpath','import')

    @staticmethod
    def get_language():
        return 'matlab'