from babelrts.components.languages.language import Language
from babelrts.components.languages.extension_pattern_action import ExtensionPatternAction

from re import compile as cmp_re

IMPORT_PATTERN = cmp_re(r'import\s+(\S+)\s*;')
IMPORT_STATIC_PATTERN = cmp_re(r'import\s+static\s+(\S+)\s*;')
PACKAGE_PATTERN = cmp_re(r'package\s+(\S+)\s*;')
EXTENDS_PATTERN = cmp_re(r'\sextends\s+(\S+)\s*')
IMPLEMENTS_PATTERN = cmp_re(r'\simplements\s+(\S+)\s*')
NEW_PATTERN = cmp_re(r'\snew\s+(\S+)\(\s*')
STATIC_PATTERN = cmp_re(r'[A-Z][\w]\.')
ANNOTATION_PATTERN = cmp_re(r'')
THROWS_PATTERN = cmp_re(r'')
CATCH_PATTERN = cmp_re(r'')

SRC_FOLDER = 'src/main/java/'
TEST_FOLDER = 'src/test/java/'
FOLDERS = (SRC_FOLDER, TEST_FOLDER)

class Java(Language):
    def get_extensions_patterns_actions(self):
        return (
            ExtensionPatternAction('.java', IMPORT_PATTERN, self.import_action),
            ExtensionPatternAction('.java', IMPORT_STATIC_PATTERN, self.import_static_action),
            ExtensionPatternAction('.java', PACKAGE_PATTERN, self.package_action),
            ExtensionPatternAction('.java', EXTENDS_PATTERN, self.used_class_action),
            ExtensionPatternAction('.java', IMPLEMENTS_PATTERN, self.multiple_used_classes_action),
            ExtensionPatternAction('.java', NEW_PATTERN, self.used_class_action),
            ExtensionPatternAction('.java', STATIC_PATTERN, self.used_class_action),
            ExtensionPatternAction('.java', ANNOTATION_PATTERN, self.used_class_action),
            ExtensionPatternAction('.java', THROWS_PATTERN, self.used_class_action),
            ExtensionPatternAction('.java', CATCH_PATTERN, self.used_class_action)
        )

    def import_action(self, match, file_path, folder_path, project_folder, content):
        if match.endswith('*'):
            path = match.replace('.', '/') + '.java'
            for folder in FOLDERS:
                return set(glob(join(project_folder, folder, path)))
        elif file := self.class_to_file(match, project_folder):
            return {file}

    def import_static_action(self, match, file_path, folder_path, project_folder, content):
        match = match.rsplit('.', 1)[0]
        if file := self.class_to_file(match, project_folder):
            return {file}

    def package_action(self, match, file_path, folder_path, project_folder, content):
        for folder in FOLDERS:
            return set(glob(join(folder_path, '*.java')))

    def used_class_action(self, match, file_path, folder_path, project_folder, content):
        if file := self.class_to_file(match, project_folder):
            return {file}

    def multiple_used_classes_action(self, match, file_path, folder_path, project_folder, content):
        return {dep for clazz in match.split(',') for dep in self.used_class(clazz, file_path, folder_path, project_folder, content)}

    def class_to_file(self, clazz, project_folder):
        clazz = clazz.replace('.', '/') + '.java'
        for folder in FOLDERS:
            if isfile(file:=join(project_folder, folder, clazz)):
                return file