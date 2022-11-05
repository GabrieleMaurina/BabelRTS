from babelrts.components.dependencies.token_language import TokenLanguage

class Groovy(TokenLanguage):

    def get_extensions(self):
        return ('groovy', 'gvy', 'gy', 'gsh')

    def get_tokens(self):
        return ('import','extends','implements','new')

    @staticmethod
    def get_language():
        return 'groovy'