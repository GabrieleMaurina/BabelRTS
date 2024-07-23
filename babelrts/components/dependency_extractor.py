from babelrts.components.dependencies.extension_pattern_action import ExtensionPatternAction
from babelrts.components.dependencies.two_way_dependency import TwoWayDependency

from babelrts.components.dependencies.languages.ada import Ada
from babelrts.components.dependencies.languages.asp import Asp
from babelrts.components.dependencies.languages.autohotkey import AutoHotkey
from babelrts.components.dependencies.languages.autoit import AutoIt
from babelrts.components.dependencies.languages.c import C
from babelrts.components.dependencies.languages.c_sharp import CSharp
from babelrts.components.dependencies.languages.cobol import Cobol
from babelrts.components.dependencies.languages.cobra import Cobra
from babelrts.components.dependencies.languages.cpp import Cpp
from babelrts.components.dependencies.languages.d import D
from babelrts.components.dependencies.languages.dart import Dart
from babelrts.components.dependencies.languages.erlang import Erlang
from babelrts.components.dependencies.languages.fortran import Fortran
from babelrts.components.dependencies.languages.go import Go
from babelrts.components.dependencies.languages.groovy import Groovy
from babelrts.components.dependencies.languages.haskell import Haskell
from babelrts.components.dependencies.languages.java import Java
from babelrts.components.dependencies.languages.javascript import Javascript
from babelrts.components.dependencies.languages.jruby import JRuby
from babelrts.components.dependencies.languages.kotlin import Kotlin
from babelrts.components.dependencies.languages.lua import Lua
from babelrts.components.dependencies.languages.matlab import MatLab
from babelrts.components.dependencies.languages.objective_c import ObjectiveC
from babelrts.components.dependencies.languages.ocaml import Ocaml
from babelrts.components.dependencies.languages.pascal import Pascal
from babelrts.components.dependencies.languages.pearl import Pearl
from babelrts.components.dependencies.languages.php import Php
from babelrts.components.dependencies.languages.prolog import Prolog
from babelrts.components.dependencies.languages.python import Python
from babelrts.components.dependencies.languages.r import R
from babelrts.components.dependencies.languages.red import Red
from babelrts.components.dependencies.languages.ruby import Ruby
from babelrts.components.dependencies.languages.rust import Rust
from babelrts.components.dependencies.languages.scala import Scala
from babelrts.components.dependencies.languages.standard_ml import StandardML
from babelrts.components.dependencies.languages.swi_prolog import SwiProlog
from babelrts.components.dependencies.languages.swift import Swift
from babelrts.components.dependencies.languages.typescript import Typescript
from babelrts.components.dependencies.languages.visual_basic import VisualBasic

from collections import defaultdict
from os.path import join, relpath, normpath, isabs, basename, dirname
from graphviz import Digraph

LANGUAGE_IMPLEMENTATIONS = (Ada, Asp, AutoHotkey, AutoIt, C, CSharp, Cobol, Cobra,
                            Cpp, D, Dart, Erlang, Fortran, Go, Groovy, Haskell, Java, Javascript, JRuby,
                            Kotlin, Lua, MatLab, ObjectiveC, Ocaml, Pascal, Pearl, Php, Prolog, Python, R,
                            Red, Ruby, Rust, Scala, StandardML, SwiProlog, Swift, Typescript, VisualBasic)


class DependencyExtractor:

    def __init__(self, babelrts, languages=None, language_implementations=None):
        self.set_babelrts(babelrts)
        self.set_languages(languages, language_implementations)
        self._dependencies = None

    def generate_dependency_graph(self):
        self._before()
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
                    self._collect_dependencies(
                        file_path, folder_path, project_folder, patterns_actions, extension, dependency_graph)
        self._add_additional_dependencies(dependency_graph, project_folder)
        self.set_dependencies(dict(dependency_graph))
        self._after()
        return self.get_dependencies()

    def _before(self):
        for language_implementation_object in self.get_language_implementation_objects():
            language_implementation_object.before()

    def _after(self):
        for language_implementation_object in self.get_language_implementation_objects():
            language_implementation_object.after()

    def safe_read(self, file):
        try:
            with open(file, 'r') as content:
                return content.read()
        except Exception:
            encodings = ('utf8', 'unicode_escape', 'ascii', 'cp932')
            for encoding in encodings:
                try:
                    with open(file, 'r', encoding=encoding) as content:
                        return content.read()
                except Exception:
                    pass
        raise UnicodeError(f'Unable to read {file}')

    def _collect_dependencies(self, file_path, folder_path, project_folder, patterns_actions, extension, dependency_graph):
        full_path = join(project_folder, file_path)
        content = self.safe_read(full_path)
        for pattern, action in patterns_actions[extension]:
            for match in pattern.findall(content):
                new_dependencies = action(
                    match, file_path, folder_path, content)
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

    def _add_additional_dependencies(self, dependency_graph, project_folder):
        for language_implementation_object in self.get_language_implementation_objects():
            additional_dependencies = language_implementation_object.get_additional_dependencies()
            if additional_dependencies:
                for file, dependencies in additional_dependencies.items():
                    if isabs(file):
                        file = relpath(file, project_folder)
                    file = normpath(file)
                    for dependency in dependencies:
                        if isabs(dependency):
                            dependency = relpath(dependency, project_folder)
                        dependency = normpath(dependency)
                        if dependency != file:
                            dependency_graph[file].add(dependency)

    def get_dependencies(self):
        if self._dependencies is None:
            self.generate_dependency_graph()
        return self._dependencies

    def set_dependencies(self, dependencies):
        self._dependencies = dependencies

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

    def get_language_implementation_objects(self):
        return self._language_implementation_objects

    def set_languages(self, languages=None, language_implementations=None):
        if not language_implementations:
            language_implementations = LANGUAGE_IMPLEMENTATIONS
        self._language_implementations = {language_implementation.get_language(
        ): language_implementation for language_implementation in language_implementations}

        if not languages:
            languages = self._language_implementations.keys()
        elif isinstance(languages, str):
            languages = (languages,)
        self._languages = languages

        self._patterns_actions = {}
        self._language_implementation_objects = []
        for language in languages:
            self._add_language_implementation(
                self._language_implementations[language.lower()])

    def _add_language_implementation(self, language_implementation):
        language_implementation_object = language_implementation(self)
        self._language_implementation_objects.append(
            language_implementation_object)
        extensions_patterns_actions = language_implementation_object.get_extensions_patterns_actions()
        if extensions_patterns_actions:
            if isinstance(extensions_patterns_actions, ExtensionPatternAction):
                self._add_extension_pattern_action(extensions_patterns_actions)
            else:
                for extension_pattern_action in extensions_patterns_actions:
                    self._add_extension_pattern_action(
                        extension_pattern_action)

    def _add_extension_pattern_action(self, extension_pattern_action):
        extension = extension_pattern_action.extension
        pattern = extension_pattern_action.pattern
        action = extension_pattern_action.action
        if extension not in self._patterns_actions:
            self._patterns_actions[extension] = [(pattern, action)]
        else:
            self._patterns_actions[extension].append((pattern, action))

    def get_extensions(self):
        return tuple(self._patterns_actions.keys())

    def visualize_digraph(self, **kwargs):
        if 'filename' not in kwargs:
            name = basename(self.get_babelrts().get_project_folder())
            if name == '.' or name == '':
                name = 'digraph'
            kwargs['filename'] = name
        if 'format' not in kwargs:
            kwargs['format'] = 'pdf'
        if 'engine' not in kwargs:
            kwargs['engine'] = 'fdp'
        if 'cleanup' not in kwargs:
            kwargs['cleanup'] = True
        if 'quiet' not in kwargs:
            kwargs['quiet'] = True
        if 'short_names' in kwargs:
            short_names = kwargs['short_names']
            del kwargs['short_names']
        else:
            short_names = False
        self.generate_digraph(short_names).render(**kwargs)

    def generate_digraph(self, short_names=True):
        g = Digraph()
        for f1, dependencies in self.get_dependencies().items():
            f1 = f1.replace('\\', '/')
            if short_names:
                f1 = basename(f1)
            g.node(f1)
            for f2 in dependencies:
                f2 = f2.replace('\\', '/')
                if short_names:
                    f2 = basename(f2)
                g.edge(f1, f2)
        return g
