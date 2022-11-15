from babelrts.components.dependencies.language import Language
from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction
from babelrts.components.dependencies.two_way_dependency import TwoWayDependency

from re import compile as cmp_re
from os.path import join, basename
from itertools import chain

INCLUDE_PATTERN = cmp_re(r'#include\s*["<](\S+?)[">]')

class C(Language):

    def get_extensions_patterns_actions(self):
        return ExtensionPatternAction('c', INCLUDE_PATTERN, self.include_action)

    @staticmethod
    def get_language():
        return 'c'

    def include_action(self, match, file_path, folder_path, content):
        dependencies = set()
        for folder in self.get_folders(folder_path):
            if self.is_file(file:=join(folder, match)):
                dependencies.add(self.check_two_way(file, file_path))
        return dependencies
                    
    def check_two_way(self, dependency, file_path):
        name = basename(file_path).rsplit('.', 1)[0]
        dependency_name = basename(dependency).rsplit('.', 1)[0]
        if name == dependency_name:
            return TwoWayDependency(dependency)
        else:
            return dependency