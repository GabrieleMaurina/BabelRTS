from babelrts.components.languages.language import Language
from babelrts.components.languages.extension_pattern_action import ExtensionPatternAction

from re import compile as cmp_re
from os.path import join

IMPORT_PATTERN = cmp_re(r'([^\S\r\n]*from[^\S\r\n]+(\S+)[^\S\r\n]+)?import[^\S\r\n](\S+)')

class Python(Language):

    def get_extensions_patterns_actions(self):
        return ExtensionPatternAction('py', IMPORT_PATTERN, self.import_action)

    def import_action(self, match, file_path, folder_path, content):
        name = match[1] if match[1] else match[2]
        path = name.replace('.', '/')
        if self.is_file(file := path + '.py'):
            return file
        elif self.is_dir(path):
            return tuple(self.expand(join(path, '*.py')))
