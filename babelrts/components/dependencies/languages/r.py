from babelrts.components.dependencies.language import Language
from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction

from re import compile as cmp_re
from os.path import join, normpath, sep

# it matches pattern like source("A1.R");source("file09.a.r") #files imported 
# retrunr only the file  name like A1.R, file09.a.r

# dependency in source file or test file like  source("../code/A1.R")
SOURCE_PATTERN = cmp_re(r'\bsource\s*\(["\']([A-Za-z0-9-_.\/]+\.[Rr])["\']\)')

# dependency in test file like source(here::here('code/example.R'))
SOURCE_HERE_PATTERN = cmp_re(r'\bsource\s*\([A-Za-z:]*\(["\']([A-Za-z0-9-_.]*\/[A-Za-z0-9-_.]+\.[Rr])["\']\)\)')


class R(Language):

    def get_extensions_patterns_actions(self):
        return (ExtensionPatternAction('R', SOURCE_PATTERN, self.source_action),
                ExtensionPatternAction('R', SOURCE_HERE_PATTERN, self.source_here_action))

    @staticmethod
    def get_language():
        return 'r'
    
    def chek_and_make_file_path(self,match,folder_path):
        # from src file
        #folder_path: ../data_analysis_1/R
        #match: '09_generate_report.R'
        
        #from test file
        #folder_path: ../data_analysis_1/tests
        #match: '../R/09_generate_report.R'
       
        # if only match has only file name then join folder name and file name ( src->src dependencies)
        if len(match.split("/"))<2:
            file=  join(folder_path,match)
        
         # if  test->src file dependcies
        else:
            src_folder = match.split("/")[-2]
            src_file = match.split("/")[-1]
            file = join('/'.join(folder_path.split("/")[:-1]),src_folder,src_file)
        
        # considering no such file depencies in src file like .. 
        # if src->src dependencies with relative path
        
        return file
    
    def source_here_action(self, match, file_path, folder_path, content):
        dependencies = []
        file = self.chek_and_make_file_path(match,folder_path)
        dependencies.append(file)
        return dependencies
    

    def source_action(self, match, file_path, folder_path, content):
        dependencies = []
        file = self.chek_and_make_file_path(match,folder_path)
        dependencies.append(file)
        return dependencies
    
