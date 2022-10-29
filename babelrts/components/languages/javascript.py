from babelrts.components.languages.language import Language
from babelrts.components.languages.extension_pattern_action import ExtensionPatternAction

from re import compile as cmp_re
from itertools import chain
from os.path import join

REQUIRE_PATTERN = cmp_re(r'require\s*\(\s*[\'"](.*)[\'"]\s*\)')
IMPORT_PATTERN = cmp_re(r'import\s[\s\S]+?\sfrom\s+[\'"](.*?)[\'"]')
EXPORT_PATTERN = cmp_re(r'export\s[\s\S]+?\sfrom\s+[\'"](.*?)[\'"]')

PATTERNS = (REQUIRE_PATTERN, IMPORT_PATTERN, EXPORT_PATTERN)

class Javascript(Language):

    def get_extensions_patterns_actions(self):
        return tuple(ExtensionPatternAction('js', pattern, self.import_action) for pattern in PATTERNS)

    def import_action(self, match, file_path, folder_path, content):
        if match.endswith('.js') or match.endswith('.ts'):
            return join(folder_path, match)
        else:
            try:
                deps = set()
                for file in chain(glob(join(folder_path, match) + '*'), glob(join(folder_path, match, '*'))):
                    if self.is_file(join(project_folder, file)) and (file.endswith('.js') or file.endswith('.ts')):
                        deps.add(file)
                return deps
            except Exception:
                pass
