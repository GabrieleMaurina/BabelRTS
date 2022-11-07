from babelrts.components.dependencies.token_language import TokenLanguage

class Cobol(TokenLanguage):

    def get_extensions(self):
        return ('cbl','cob','cpy')

    def get_tokens(self):
        return ('copy','COPY')

    @staticmethod
    def get_language():
        return 'cobol'