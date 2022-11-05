from babelrts.components.dependencies.token_language import TokenLanguage

class Scala(TokenLanguage):

    def get_extensions(self):
        return 'scala'

    def get_tokens(self):
        return ('import','new','extends')

    @staticmethod
    def get_language():
        return 'scala'