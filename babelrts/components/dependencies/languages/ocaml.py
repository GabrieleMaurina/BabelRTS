from babelrts.components.dependencies.token_language import TokenLanguage

class Ocaml(TokenLanguage):

    def get_extensions(self):
        return ('ml','mli')

    def get_tokens(self):
        return ('open','use','new')

    @staticmethod
    def get_language():
        return 'ocaml'