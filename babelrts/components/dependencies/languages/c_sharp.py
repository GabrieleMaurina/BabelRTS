from babelrts.components.dependencies.language import Language
from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction

from re import compile as cmp_re
from collections import defaultdict

NAMESPACE_PATTERN = cmp_re(r'\bnamespace\s+(\S+?)\s*[{;]')
#using has two different declaration: directive and
USING_DIRECTIVE_PATTERN = cmp_re(r'\busing\s+(\S+?)\s*;')
INHERIT_PATTERN = cmp_re(r'\bclass\s+(\S+?)\s*\:\s+([\s\S]+?)\s*{')
NEW_PATTERN = cmp_re(r'\bnew\s+(\S+?)\s*\(\s*')

THROW_PATTERN = cmp_re(r'\bthrow\s+([\s\S]+?)\s*;')
CATCH_PATTERN = cmp_re(r'\bcatch\s*\(\s*([\s\S]+?)\s*\S+\)')

class CSharp(Language):

#NOTE: IS THIS REQUIRED?
    # def __init__(self, dependency_extractor):
    #     super().__init__(dependency_extractor)
    #     self._reset()

    def get_extensions_patterns_actions(self):
        return  (
            ExtensionPatternAction('cs', NAMESPACE_PATTERN, self.namespace_action),
            ExtensionPatternAction('cs', USING_DIRECTIVE_PATTERN, self.using_action),
        )

    @staticmethod
    def get_language():
        return 'c#'

    def namespace_action(self, match, file_path, folder_path, content):
        namespaces = match.split('.')

        self._dependencies[file_path].add(namespaces[-1])
        self._namespaces[namespaces[-1]].add(file_path)

    def using_action(self, match, file_path, folder_path, content):
        namespaces = match.split('.')

        self._dependencies[file_path].add(namespaces[-1])
        if len(namespaces)>1:
            self._dependencies[file_path].add(namespaces[-2])

    def get_additional_dependencies(self):
        additional_dependencies = defaultdict(set)
        for file, namespaces in self._dependencies.items():
            for namespace in namespaces:
                additional_dependencies[file].update(self._namespaces[namespace])
        self._reset()
        return additional_dependencies

#NOTE: IS THIS REQUIRED?
    # def _reset(self):
    #     self._dependencies = defaultdict(set)
    #     self._namespaces = defaultdict(set)