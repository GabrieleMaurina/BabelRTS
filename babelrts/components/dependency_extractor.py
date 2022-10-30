from babelrts.components.languages.java import Java
from babelrts.components.languages.python import Python
from babelrts.components.languages.javascript import Javascript
from babelrts.components.languages.typescript import Typescript
from babelrts.components.languages.extension_pattern_action import ExtensionPatternAction

from collections.abc import Iterable
from os.path import join, relpath, normpath, isabs, basename, dirname

LANGUAGE_IMPLEMENTATIONS = (Java, Python, Javascript, Typescript)

class DependencyExtractor:

    def __init__(self, babelrts, languages=None, language_implementations=None):
        self._babelrts = babelrts
        self._dependency_graph = None
        self.set_languages(languages, language_implementations)

    def generate_dependency_graph(self):
        all_files = self.get_babelrts().get_change_discoverer().get_all_files()
        extensions = self.get_extensions()
        patterns_actions = self.get_patterns_actions()
        project_folder = self.get_babelrts().get_project_folder()
        self._dependency_graph = {}
        for file_path in all_files:
            file = basename(file_path)
            folder_path = dirname(file_path)
            split = file.rsplit('.', 1)
            if len(split) == 2:
                name, extension = split
                if name and extension and extension in extensions:
                    self._collect_dependencies(file_path, folder_path, project_folder, patterns_actions, extension)
        return self._dependency_graph

    def _collect_dependencies(self, file_path, folder_path, project_folder, patterns_actions, extension):
        with open(join(project_folder, file_path), 'r', encoding='unicode_escape') as content:
            content = content.read()
        dependencies = set()
        for pattern, action in patterns_actions[extension]:
            for match in pattern.findall(content):
                new_dependencies = action(match, file_path, folder_path, content)
                if new_dependencies:
                    if isinstance(new_dependencies, str):
                        new_dependencies = (new_dependencies,)
                    #print(type(new_dependencies))
                    #for d in new_dependencies:
                    #    print('\t', type(d), d)
                    dependencies.update(path for path in (normpath(relpath(dependency, project_folder) if isabs(dependency) else normpath(dependency)) for dependency in new_dependencies) if path!=file_path)
        if dependencies:
            self._dependency_graph[file_path] = tuple(dependencies)

    def get_dependency_graph(self):
        return self._dependency_graph

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