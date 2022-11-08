from babelrts.components.dependencies.token_language import TokenLanguage

class ObjectiveC(TokenLanguage):

    def get_extensions(self):
        return ('h','m','mm','M')

    def get_tokens(self):
        return ('#import','#include')

    @staticmethod
    def get_language():
        return 'objective-c'
