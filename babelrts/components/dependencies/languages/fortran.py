from babelrts.components.dependencies.token_language import TokenLanguage

class Fortran(TokenLanguage):

    def get_extensions(self):
        return ('f','F','for','FOR','f77','f90','f95','fpp')

    def get_tokens(self):
        return ('include','use')

    @staticmethod
    def get_language():
        return 'fortran'