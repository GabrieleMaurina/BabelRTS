from babelrts.components.dependencies.language import Language
from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction

from re import compile as cmp_re
from os.path import join, relpath, normpath
from os import sep
from pygtrie import StringTrie

IMPORT_PATTERN = cmp_re(r'\bimport\s+(\S+)\s*;')
IMPORT_STATIC_PATTERN = cmp_re(r'\bimport\s+static\s+(\S+)\s*;')
PACKAGE_PATTERN = cmp_re(r'\bpackage\s+(\S+)\s*;')
EXTENDS_PATTERN = cmp_re(r'\bextends\s+([\s\S]+?)\s*(?:{|implements)')
IMPLEMENTS_PATTERN = cmp_re(r'\bimplements\s+([\s\S]+?)\s*(?:{|extends)')
NEW_PATTERN = cmp_re(r'\bnew\s+(\S+?)\s*\(\s*')
STATIC_PATTERN = cmp_re(r'\b([A-Za-z_\.]+?)\.')
ANNOTATION_PATTERN = cmp_re(r'(?<!\S)@(\w+)')
THROWS_PATTERN = cmp_re(r'\bthrows\s+([A-Za-z_\., ]+?)\s*{')
CATCH_PATTERN = cmp_re(r'\bcatch\s*\(\s*([A-Za-z_\.| ]+?)\s*\S+\)')

SPLIT = cmp_re(r',|\||\n')
SPLIT_PATH = cmp_re(r'\\|\/')

class Java(Language):
    def get_extensions_patterns_actions(self):
        return (
            ExtensionPatternAction('java', IMPORT_PATTERN, self.import_action),
            ExtensionPatternAction('java', IMPORT_STATIC_PATTERN, self.import_static_action),
            #ExtensionPatternAction('java', PACKAGE_PATTERN, self.package_action),
            ExtensionPatternAction('java', EXTENDS_PATTERN, self.multiple_used_classes_action),
            ExtensionPatternAction('java', IMPLEMENTS_PATTERN, self.multiple_used_classes_action),
            ExtensionPatternAction('java', NEW_PATTERN, self.used_class_action),
            ExtensionPatternAction('java', STATIC_PATTERN, self.used_class_action),
            ExtensionPatternAction('java', ANNOTATION_PATTERN, self.used_class_action),
            ExtensionPatternAction('java', THROWS_PATTERN, self.multiple_used_classes_action),
            ExtensionPatternAction('java', CATCH_PATTERN, self.multiple_used_classes_action)
        )

    @staticmethod
    def get_language():
        return 'java'

    def import_action(self, match, file_path, folder_path, content):
        if match.endswith('*'):
            match = match[:-2]
        return self.class_to_files(match, file_path)

    def import_static_action(self, match, file_path, folder_path, content):
        match = match.rsplit('.', 1)[0]
        return self.class_to_files(match, file_path)

    def package_action(self, match, file_path, folder_path, content):
        return self.class_to_files(match, file_path)

    def used_class_action(self, match, file_path, folder_path, content):
        return self.class_to_files(match, file_path)

    def multiple_used_classes_action(self, match, file_path, folder_path, content):
        clazzes = (clazz for clazz in (v.strip() for v in SPLIT.split(match)) if clazz)
        return (file for clazz in clazzes for file in self.class_to_files(clazz, file_path))
    
    def get_files_for_class(self, clazz):
        if clazz in self.classes or self.classes.has_subtrie(clazz):
            return tuple(file for files in self.classes[clazz:] for file in files)
        else:
            return ()

    def class_to_files(self, clazz, file_path):
        files = self.get_files_for_class(clazz)
        if not files:
            package = self.packages[file_path]
            package_class = f'{package}.{clazz}'
            files = self.get_files_for_class(package_class)
        return files

    def before(self):
        self.classes = StringTrie(separator='.')
        self.packages = {}
        folders = tuple(self.get_source_test_folders())
        files = self.get_all_files()
        for file in files:
            clazz = self._find_clazz(file, folders)
            if clazz in self.classes:
                self.classes[clazz].append(file)
            else:
                self.classes[clazz] = [file]
            self.packages[file] = clazz.rsplit('.', 1)[0]
    
    def _find_clazz(self, file, folders):
        size = max([len(folder) for folder in folders if file.startswith(folder)])
        clazz = file[size + 1:-5].replace(sep, '.')
        return clazz
