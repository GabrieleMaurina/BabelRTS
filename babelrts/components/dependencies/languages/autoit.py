from babelrts.components.dependencies.token_language import TokenLanguage

class AutoIt(TokenLanguage):

    def get_extensions(self):
        return 'su3'

    def get_tokens(self):
        return '#include'

    @staticmethod
    def get_language():
        return 'autoit'