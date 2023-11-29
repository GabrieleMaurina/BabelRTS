from babelrts.components.dependencies.language import Language
from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction

from re import compile as cmp_re
from os.path import join, normpath, sep

# it matches pattern like source("A1.R");source("file09.a.r") #files imported 
# retrunr only the file  name like A1.R, file09.a.r

SOURCE_PATTERN = cmp_re(r'source\s*\("([A-Za-z0-9_-.]+\.[R|r])"\)') 
class R(Language):

    def get_extensions_patterns_actions(self):
        return ExtensionPatternAction('r', SOURCE_PATTERN, self.source_action)

    @staticmethod
    def get_language():
        return 'r'
    
    def source_action(self, match, file_path, folder_path, content):
        print (match)
        dependencies = set()
        for folder in self.get_folders(folder_path):
            if self.is_file(file:=join(folder, match)):
                dependencies.add(self.check_two_way(file, file_path))
        return dependencies