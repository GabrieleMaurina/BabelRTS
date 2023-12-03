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

# Dependency in gloabl scope like calling sum() from A.R file inside B.R without any imports
# for such cases, we need to look inside NAMESPACE for possible match of file name corresponding to that function sum()
FUNCTION_CALLING_PATTERN = cmp_re(r'\b([A-Za-z0-9-_.]+)\s*\(')


class R(Language):

    def get_extensions_patterns_actions(self):
        return (ExtensionPatternAction('R', SOURCE_PATTERN, self.source_action),
                ExtensionPatternAction('R', SOURCE_HERE_PATTERN, self.source_here_action),
                ExtensionPatternAction('R', FUNCTION_CALLING_PATTERN, self.function_calling_action))

    @staticmethod
    def get_language():
        return 'r'
    
    def is_r_keyword(self,word):
        keywords = ['if','else','function','return','class','source','context','for','while','next','c','print','sum','min','max','str','length','mean','library','package','test_that','list','tryCatch']
        if word in keywords:
            return True
        return False
    
    def chek_and_make_file_path(self,match,folder_path):
        # from src file
        #folder_path: ../data_analysis_1/R
        #match: '09_generate_report.R'
        
        #from test file
        #folder_path: ../data_analysis_1/tests
        #match: '../R/09_generate_report.R'
       
        # if match has only file name (possible for src->src dependencies) then join folder name and file name 
        if len(match.split("/"))<2:
            file=  join(folder_path,match)
        
         # if  test->src file dependcies
        else:
            src_folder = match.split("/")[-2]
            src_file = match.split("/")[-1]
            file = join('/'.join(folder_path.split("/")[:-1]),src_folder,src_file)
        
        if self.is_file(file):
            return file
        
        # check if the file is available inside any other folder
        for folder in self.get_folders(folder_path):
            file = join(folder,match.split("/")[-1])
            #print("folder: + "+folder)
            if self.is_file(file):
                print("yes: "+file)
                return file
        
        return None
    
    def check_namespace_entries(self,match,file_path,folder_path):
        
        return 
    
    def search_file_in_directory(self,match,file_path,folder_path,content):
        if self.is_r_keyword(match):
            return None
        
        for folder in self.get_folders(folder_path):
            file = join(folder,match+'.R')
            if self.is_file(file):
                return file
            
        return None
    
    def check_function_assignment(self,match,content):
        FUNCTION_ASSIGNMENT_PATTERN = cmp_re(r'{}[=<-]'.format(match))
        return

    def source_here_action(self, match, file_path, folder_path, content):
        dependencies = []
        file = self.chek_and_make_file_path(match,folder_path)
        dependencies.append(file)
        return dependencies
    

    def source_action(self, match, file_path, folder_path, content):
        dependencies = []
        file = self.chek_and_make_file_path(match,folder_path)
        if file is not None:
            dependencies.append(file)
        return dependencies
    
    def function_calling_action(self, match, file_path, folder_path, content):
        dependencies = []
        file = self.search_file_in_directory(match,folder_path)
        if file is not None:
            dependencies.append(file)
        return dependencies
    
