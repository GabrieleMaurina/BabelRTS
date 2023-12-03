import ntpath
from babelrts.components.dependencies.language import Language
from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction

from re import compile as cmp_re
from collections import defaultdict
from os import sep

NAMESPACE_PATTERN = cmp_re(r'\bnamespace\s+(\S+?)\s*[{;]')
#using has two different declaration: directive and
USING_DIRECTIVE_PATTERN = cmp_re(r'\busing\s+(\S+?)\s*;')
INHERIT_PATTERN = cmp_re(r'\bclass\s+(\S+?)\s*\:\s+([\s\S]+?)\s*{')
NEW_PATTERN = cmp_re(r'\bnew\s+(\S+?)\s*\(\s*')

THROW_PATTERN = cmp_re(r'\bthrow\s+([\s\S]+?)\s*;')
CATCH_PATTERN = cmp_re(r'\bcatch\s*\(\s*([\s\S]+?)\s*\S+\)')

class CSharp(Language):


    def __init__(self, dependency_extractor):
        super().__init__(dependency_extractor)
        self._reset()

    def get_extensions_patterns_actions(self):
        return  (
            ExtensionPatternAction('cs', NAMESPACE_PATTERN, self.namespace_action),
            ExtensionPatternAction('cs', USING_DIRECTIVE_PATTERN, self.using_action),
            ExtensionPatternAction('cs', INHERIT_PATTERN, self.inherit_action),
        )

    @staticmethod
    def get_language():
        return 'c#'

    def namespace_action(self, match, file_path, folder_path, content):
        namespaces = match.split('.')

        self._dependencies[file_path].add(namespaces[-1])
        # self._namespaces[namespaces[-1]].add(file_path)

    def using_action(self, match, file_path, folder_path, content):
        head, tail = ntpath.split(self._sourceFolder)

        rootUsing = match.rsplit('.', 1)[0]
        usingPath = match.replace('.', sep)

        if tail == rootUsing:
            # Make this part more well written..?
            pathToScopedFolder = usingPath
            if head != "":
                pathToScopedFolder = head + sep + usingPath
        else:
            pathToScopedFolder = self._sourceFolder + sep + usingPath

        if self.is_dir(pathToScopedFolder):
            self._using[file_path].add(pathToScopedFolder)

        return self.getAllFilesFromFolder(pathToScopedFolder)

    # TO DO-LATER: Use string similarity to check if two names are similar
    # enough to be considered the same word. Such as ExitActionBehavior and ExitActionBehaviour
    def inherit_action(self, match, file_path, folder_path, content):
        inheritedClasses = match[1].rsplit(', ', 1)
        classesInherited = []

        for inherited in inheritedClasses:
            path = self.findPathForClass(inherited, file_path, folder_path)
            if path is not None:
                classesInherited.append(path)

        return classesInherited

    def new_action(self, match, file_path, folder_path, content):
        return 0

    #NOTE: We're going to ignore interfaces. It seems a bit more complicated
    # to find them via file names. The files themselves have to be read.
    def findPathForClass(self, className, file_path, folder_path):
        if className[0] != 'I' or className[1].islower():
            inheritedPath = sep + className + ".cs"

            if self.is_file(folder_path + inheritedPath):
                return folder_path + inheritedPath
            else:
                for usingPath in self._using[file_path]:
                    if self.is_file(usingPath + inheritedPath):
                        return usingPath + inheritedPath
    def getAllFilesFromFolder(self, pathToScopedFolder):
        files = []

        if self.is_dir(pathToScopedFolder):
            for file in self.get_all_files():
                if pathToScopedFolder in file:
                    files.append(file)

        return files

    def get_additional_dependencies(self):
            additional_dependencies = defaultdict(set)
            for file, namespaces in self._dependencies.items():
                for namespace in namespaces:
                    additional_dependencies[file].update(self._namespaces[namespace])
            self._reset()
            return additional_dependencies

#NOTE: IS THIS REQUIRED?
    def _reset(self):
        self._sourceFolder = list(self.get_source_test_folders())[0]
        self._using = defaultdict(set)
        self._dependencies = defaultdict(set)
        self._namespaces = defaultdict(set)