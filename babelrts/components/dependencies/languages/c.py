from babelrts.components.dependencies.language import Language
from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction
from babelrts.components.dependencies.two_way_dependency import TwoWayDependency

from re import compile as cmp_re
from os.path import join, basename

INCLUDE_PATTERN = cmp_re(r'#include (["<].+?[">])')

class C(Language):

    def get_extensions_patterns_actions(self):
        return ExtensionPatternAction('c', INCLUDE_PATTERN, self.include_action)

    @staticmethod
    def get_language():
        return 'c'

    def include_action(self, match, file_path, folder_path, content):
        quotes = match[0] == '"'
        match = match[1:-1]
        if quotes:
            if self.is_file(file:=join(folder_path, match)):
                return self.check_two_way(file, file_path)
        else:
            if self.is_file(match):
                return self.check_two_way(match, file_path)
                    
    def check_two_way(self, match, file_path):
        name = basename(file_path).rsplit('.', 1)[0]
        match_name = basename(match).rsplit('.', 1)[0]
        if name == match_name:
            return TwoWayDependency(file)
        else:
            return file