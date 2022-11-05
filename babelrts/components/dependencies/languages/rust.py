from babelrts.components.dependencies.token_language import TokenLanguage

class Rust(TokenLanguage):

    def get_extensions(self):
        return 'rs'

    def get_tokens(self):
        return ('include','use')

    @staticmethod
    def get_language():
        return 'rust'