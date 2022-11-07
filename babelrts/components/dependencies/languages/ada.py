from babelrts.components.dependencies.token_language import TokenLanguage

class Ada(TokenLanguage):

    def get_extensions(self):
        return ('adb','ads')

    def get_tokens(self):
        return 'with'

    @staticmethod
    def get_language():
        return 'ada'