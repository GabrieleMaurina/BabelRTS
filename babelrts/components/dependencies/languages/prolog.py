from babelrts.components.dependencies.token_language import TokenLanguage

class Prolog(TokenLanguage):

    def get_extensions(self):
        return ('pl','pro','P')

    def get_tokens(self):
        return ('-include','-use_module')

    @staticmethod
    def get_language():
        return 'prolog'