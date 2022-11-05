from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction
from babelrts.components.dependencies.two_way_dependency import TwoWayDependency
from babelrts.components.dependencies.languages.c import C
from babelrts.components.dependencies.languages.c_sharp import CSharp
from babelrts.components.dependencies.languages.cpp import Cpp
from babelrts.components.dependencies.languages.erlang import Erlang
from babelrts.components.dependencies.languages.go import Go
from babelrts.components.dependencies.languages.groovy import Groovy
from babelrts.components.dependencies.languages.java import Java
from babelrts.components.dependencies.languages.javascript import Javascript
from babelrts.components.dependencies.languages.kotlin import Kotlin
from babelrts.components.dependencies.languages.php import Php
from babelrts.components.dependencies.languages.python import Python
from babelrts.components.dependencies.languages.ruby import Ruby
from babelrts.components.dependencies.languages.rust import Rust
from babelrts.components.dependencies.languages.scala import Scala
from babelrts.components.dependencies.languages.swift import Swift
from babelrts.components.dependencies.languages.typescript import Typescript

from collections import defaultdict
from collections.abc import Iterable
from os.path import join, relpath, normpath, isabs, basename, dirname

LANGUAGE_IMPLEMENTATIONS = (C, CSharp, Cpp, Erlang, Go, Groovy, Java, Javascript, Kotlin, Php, Python, Ruby, Rust, Scala, Swift, Typescript)

class DependencyExtractor:

    def __init__(self, babelrts, languages=None, language_implementations=None):
        self.set_babelrts(babelrts)
        self.set_languages(languages, language_implementations)
        self._dependency_graph = None

    def generate_dependency_graph(self):
        all_files = self.get_babelrts().get_change_discoverer().get_all_files()
        extensions = self.get_extensions()
        patterns_actions = self.get_patterns_actions()
        project_folder = self.get_babelrts().get_project_folder()
        dependency_graph = defaultdict(set)
        for file_path in all_files:
            file = basename(file_path)
            folder_path = dirname(file_path)
            split = file.rsplit('.', 1)
            if len(split) == 2:
                name, extension = split
                if name and extension and extension in extensions:
                    self._collect_dependencies(file_path, folder_path, project_folder, patterns_actions, extension, dependency_graph)
        self.set_dependency_graph(dict(dependency_graph))
        return self.get_dependency_graph()

    def _collect_dependencies(self, file_path, folder_path, project_folder, patterns_actions, extension, dependency_graph):
        full_path = join(project_folder, file_path)
        try:
            with open(full_path, 'r', encoding='utf-8') as content:
                content = content.read()
        except Exception:
            with open(full_path, 'r', encoding='unicode_escape') as content:
                content = content.read()
        for pattern, action in patterns_actions[extension]:
            for match in pattern.findall(content):
                new_dependencies = action(match, file_path, folder_path, content)
                if new_dependencies:
                    if isinstance(new_dependencies, str):
                        new_dependencies = (new_dependencies,)
                    for dependency in new_dependencies:
                        if isabs(dependency):
                            dependency = relpath(dependency, project_folder)
                        dependency = normpath(dependency)
                        if dependency != file_path:
                            dependency_graph[file_path].add(dependency)
                            if isinstance(dependency, TwoWayDependency):
                                dependency_graph[dependency].add(file_path)

    def get_dependency_graph(self):
        return self._dependency_graph

    def set_dependency_graph(self, dependency_graph):
        self._dependency_graph = dependency_graph

    def get_babelrts(self):
        return self._babelrts

    def set_babelrts(self, babelrts):
        self._babelrts = babelrts

    def get_languages(self):
        return self._languages

    def get_language_implementations(self):
        return tuple(self._language_implementations.values())
    
    def get_patterns_actions(self):
        return self._patterns_actions

    def set_languages(self, languages=None, language_implementations=None):
        if not language_implementations:
            language_implementations = LANGUAGE_IMPLEMENTATIONS
        self._language_implementations = {language_implementation.get_language():language_implementation for language_implementation in language_implementations}

        if not languages:
            languages = self._language_implementations.keys()
        elif isinstance(languages, str):
            languages = (languages,)
        self._languages = languages

        self._patterns_actions = {}
        for language in languages:
            self._add_language_implementation(self._language_implementations[language.lower()])

    def _add_language_implementation(self, language_implementation):
        extensions_patterns_actions = language_implementation(self).get_extensions_patterns_actions()
        if extensions_patterns_actions:
            if isinstance(extensions_patterns_actions, ExtensionPatternAction):
                self._add_extension_pattern_action(extensions_patterns_actions)
            else:
                for extension_pattern_action in extensions_patterns_actions:
                    self._add_extension_pattern_action(extension_pattern_action)

    def _add_extension_pattern_action(self, extension_pattern_action):    
        extension = extension_pattern_action.extension
        pattern = extension_pattern_action.pattern
        action = extension_pattern_action.action
        if extension not in self._patterns_actions:
            self._patterns_actions[extension] = [(pattern, action)]
        else:
            self._patterns_actions[extension].append((pattern, action))

    def get_extensions(self):
        return self._patterns_actions.keys()