from babelrts.components.dependencies.token_language import TokenLanguage

class Lua(TokenLanguage):

    def get_extensions(self):
        return 'lua'

    def get_tokens(self):
        return 'require'

    @staticmethod
    def get_language():
        return 'lua'