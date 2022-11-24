from babelrts.components.dependencies.language import Language
from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction

from re import compile as cmp_re
from os.path import join, normpath, sep

IMPORT_PATTERN = cmp_re(r'(?<!\S)(?:from\s+(\S+)\s+)?import\s+(.+)\s*?\n')

class Python(Language):

    def get_extensions_patterns_actions(self):
        return ExtensionPatternAction('py', IMPORT_PATTERN, self.import_action)

    @staticmethod
    def get_language():
        return 'python'

    def check_relative_import(self, string, folder_path):
        string, dots = self.remove_leading_dots(string)
        if dots == 1:
            path =  join(folder_path, string)
        elif dots > 1:
            folders = normpath(folder_path).split(sep)
            path =  sep.join(folders[:1-dots])
        else:
            path = string
        return path.replace('.', sep)

    def remove_leading_dots(self, string):
        i = 0
        while i < len(string) and string[i] == '.':
            i += 1
        return string[i:], i

    def import_dependencies(self, path, rec=True):
        if self.is_file(file := path + '.py'):
            return [file]
        elif self.is_dir(path):
            files = list(self.expand(join(path, '*.py')))
            if self.is_file(file := path + '__init__.py'):
                files.append(file)
            return files
        elif rec:
            return self.import_dependencies(path.rsplit(sep, 1)[0], False)

    def import_action(self, match, file_path, folder_path, content):
        if match[0]:
            first = self.check_relative_import(match[0], folder_path)
            second = (v.strip() for v in match[1].split(','))
            paths = tuple(join(first, v) for v in second)
            dependencies = []
            for path in paths:
                if files := self.import_dependencies(path):
                    dependencies += files
            return dependencies
        else:
            return self.import_dependencies(self.check_relative_import(match[1], folder_path))