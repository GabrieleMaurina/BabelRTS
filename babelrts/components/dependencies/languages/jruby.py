from babelrts.components.dependencies.languages import Ruby

class JRuby(Ruby):

    def get_tokens(self):
        return super().get_tokens() + ('java_import', 'include_class', 'import')

    @staticmethod
    def get_language():
        return 'jruby'