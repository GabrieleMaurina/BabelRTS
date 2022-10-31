from babelrts.components.dependencies.language import Language
from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction

from re import compile as cmp_re
from itertools import chain
from os.path import join

REQUIRE_PATTERN = cmp_re(r'(?<!\S)require\s*\(\s*[\'"](.*)[\'"]\s*\)')
IMPORT_PATTERN = cmp_re(r'(?<!\S)import\s[\s\S]+?\sfrom\s+[\'"](.*?)[\'"]')
EXPORT_PATTERN = cmp_re(r'(?<!\S)export\s[\s\S]+?\sfrom\s+[\'"](.*?)[\'"]')

PATTERNS = (REQUIRE_PATTERN, IMPORT_PATTERN, EXPORT_PATTERN)

class Javascript(Language):

    def get_extensions_patterns_actions(self):
        return tuple(ExtensionPatternAction('js', pattern, self.import_action) for pattern in PATTERNS)

    @staticmethod
    def get_language():
        return 'javascript'

    def import_action(self, match, file_path, folder_path, content):
        if match.endswith('.js') or match.endswith('.ts'):
            if self.is_file(file:=join(folder_path, match)):
                return file
        else:
            try:
                deps = set()
                for file in chain(self.expand(join(folder_path, match) + '*'), self.expand(join(folder_path, match, '*'))):
                    if self.is_file(file) and (file.endswith('.js') or file.endswith('.ts')):
                        deps.add(file)
                return deps
            except Exception:
                pass
