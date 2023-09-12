from babelrts.components.dependencies.language import Language
from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction
from babelrts.components.dependencies.two_way_dependency import TwoWayDependency

from re import compile as cmp_re
from os.path import join, basename, commonprefix

INCLUDE_PATTERN = cmp_re(r'#include\s*["<](\S+?)[">]')
START_PATTERN = cmp_re(r'^')

class C(Language):

    def get_extensions_patterns_actions(self):
        return (ExtensionPatternAction('c', INCLUDE_PATTERN, self.include_action),
                ExtensionPatternAction('c', START_PATTERN, self.naming_convention_action))

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

    def naming_convention_action(self, match, file_path, folder_path, content):
        dependencies = set()
        file_name = basename(file_path)
        file_name_len = len(file_name)
        files = self.get_dependency_extractor().get_babelrts().get_change_discoverer().get_all_files()
        files = (file for file in files if file.startswith(folder_path) and file != file_path)
        for file in files:
            name = basename(file)
            common = len(commonprefix((file_name, name)))
            if common > 6 and common > file_name_len * 0.75:
                dependencies.add(file)
        return dependencies

