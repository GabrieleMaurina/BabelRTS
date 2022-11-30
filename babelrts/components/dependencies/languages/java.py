from babelrts.components.dependencies.language import Language
from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction

from re import compile as cmp_re
from os.path import join, relpath, normpath
from os import sep

IMPORT_PATTERN = cmp_re(r'\bimport\s+(\S+)\s*;')
IMPORT_STATIC_PATTERN = cmp_re(r'\bimport\s+static\s+(\S+)\s*;')
PACKAGE_PATTERN = cmp_re(r'\bpackage\s+(\S+)\s*;')
EXTENDS_PATTERN = cmp_re(r'\bextends\s+([\s\S]+?)\s*(?:{|implements)')
IMPLEMENTS_PATTERN = cmp_re(r'\bimplements\s+([\s\S]+?)\s*(?:{|extends)')
NEW_PATTERN = cmp_re(r'\bnew\s+(\S+?)\s*\(\s*')
STATIC_PATTERN = cmp_re(r'\b([A-Z]\S+?)\.')
ANNOTATION_PATTERN = cmp_re(r'(?<!\S)@(\S+)(?:\s*\()?')
THROWS_PATTERN = cmp_re(r'\bthrows\s+([\s\S]+?)\s*{')
CATCH_PATTERN = cmp_re(r'\bcatch\s*\(\s*([\s\S]+?)\s*\S+\)')

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
            path = match.replace('.', '/') + '.java'
            return (file for folder in self.get_source_test_folders() for file in self.expand(join(folder, path)))
        else:
            return self.class_to_files(match, folder_path)

    def import_static_action(self, match, file_path, folder_path, content):
        match = match.rsplit('.', 1)[0]
        return self.class_to_files(match, folder_path)

    def package_action(self, match, file_path, folder_path, content):
        return (file for folder in self.get_source_test_folders() for file in self.expand(join(folder_path, '*.java')))

    def used_class_action(self, match, file_path, folder_path, content):
        return self.class_to_files(match, folder_path)

    def multiple_used_classes_action(self, match, file_path, folder_path, content):
        clazzes = (clazz for clazz in (v.strip() for v in SPLIT.split(match)) if clazz)
        return (file for clazz in clazzes for file in self.class_to_files(clazz, folder_path))

    def fix_path(self, path):
        tokens = SPLIT_PATH.split(normpath(path))
        tokens = (v.strip() for v in tokens)
        tokens = (v for v in tokens if v)
        return sep.join(tokens)

    def get_package_path(self, folder):
        folder = self.fix_path(folder)
        for path in self.get_source_test_folders():
            path = self.fix_path(path) + sep
            if folder.startswith(path):
                return relpath(folder, path)

    def class_to_files(self, clazz, folder_path):
        class_path = clazz.replace('.', sep) + '.java'
        package_path = self.get_package_path(folder_path)

        if package_path:
            packages = ('', package_path)
        else:
            packages = ('',)

        folders = self.get_source_test_folders()

        paths = (join(folder, package, class_path) for folder in folders for package in packages)

        return (path for path in paths if self.is_file(path))
