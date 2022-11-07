from babelrts.components.dependencies.token_language import TokenLanguage

class AutoHotkey(TokenLanguage):

    def get_extensions(self):
        return 'ahk'

    def get_tokens(self):
        return '#include'

    @staticmethod
    def get_language():
        return 'autohotkey'