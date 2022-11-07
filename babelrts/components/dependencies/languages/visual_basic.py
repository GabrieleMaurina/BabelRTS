from babelrts.components.dependencies.token_language import TokenLanguage

class VisualBasic(TokenLanguage):

    def get_extensions(self):
        return 'vb'

    def get_tokens(self):
        return 'Imports'

    @staticmethod
    def get_language():
        return 'visualbasic'