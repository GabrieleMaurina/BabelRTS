from babelrts.components.dependencies.token_language import TokenLanguage

class Ruby(TokenLanguage):

    def get_extensions(self):
        return 'rb'

    def get_tokens(self):
        return ('load','require','include','extend','prepend', 'java_import', 'include_class', 'import')

    @staticmethod
    def get_language():
        return ('ruby', 'jruby')