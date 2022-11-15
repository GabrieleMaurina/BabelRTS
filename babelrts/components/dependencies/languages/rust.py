from babelrts.components.dependencies.language import Language
from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction

from re import compile as cmp_re
from os.path import join

IMPORT_PATTERN = cmp_re(r'(?<!\S)(?:mod|use)\s+(\S+?)[\s;{]')

class Rust(Language):

    def get_extensions_patterns_actions(self):
        return ExtensionPatternAction('rs', IMPORT_PATTERN, self.import_action)

    @staticmethod
    def get_language():
        return 'rust'

    def import_action(self, match, file_path, folder_path, content):
        path = match.replace('::', '/')
        dependencies = self.get_module_dependencies(path, folder_path)
        if not dependencies:
            dependencies = self.get_module_dependencies(path.rsplit('/', 1)[0], folder_path)
        return dependencies

    def get_module_dependencies(self, path, folder_path):
        if self.is_file(file := join(folder_path, path + '.rs')):
            return file
        elif self.is_dir(path):
            return tuple(self.expand(join(folder_path, path, '*.rs')))