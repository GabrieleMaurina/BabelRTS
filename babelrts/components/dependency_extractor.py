from babelrts.components.languages.java import Java
from babelrts.components.languages.python import Python
from babelrts.components.languages.javascript import Javascript
from babelrts.components.languages.typescript import Typescript

from collections.abc import Iterable

LANGUAGE_IMPLEMENTATIONS = {'java': Java, 'python': Python, 'javascript': Javascript, 'typescript': Typescript}

class DependencyExtractor:

    def __init__(self, babelrts, languages=None, language_implementations=None):
        self._babelrts = babelrts
        self._dependency_graph = None
        self.set_languages(languages, language_implementations)

    def generate_dependency_graph(self):
        all_files = self.get_babelrts().get_change_discoverer().get_all_files()
        extensions = self.get_extensions()
        patterns_actions = self.get_patterns_actions()
        self._dependency_grap = {}
        for file_path in all_files:
            file = basename(file_path)
            folder_path = dirname(file_path)
            split = file.rsplit('.', 1)
            if len(split) == 2:
                name, extension = split
                if name and extension and extension in extensions:
                    with open(file_path, 'r', encoding='unicode_escape') as content:
                        content = content.read()
                    dependencies = set()
                    for pattern, action in patterns_actions[extension]:
                        for match in pattern.findall(content):
                            new_depenencies = action(match, file_path, folder_path, content)
                            if new_depenencies:
                                if isinstance(new_dependencies, str):
                                    new_depenencies = (new_depenencies,)
                                dependencies.update({path for path in (normpath(relpath(dependency, project_folder)) for dependency in new_depenencies) if path!=file_path})
                    if dependencies:
                        self._dependency_grap[file_path] = tuple(dependencies)
        return self._dependency_grap

    def get_dependency_graph(self):
        return self._dependency_graph

    def get_babelrts(self):
        return self._babelrts

    def set_babelrts(self, babelrts):
        self._babelrts = babelrts

    def get_languages(self):
        return self._languages

    def get_language_implementations(self):
        return self._language_implementations
    
    def get_patterns_actions(self):
        return self._patterns_actions

    def set_languages(self, languages=None, language_implementations=None):
        if not language_implementations:
            language_implementations = LANGUAGE_IMPLEMENTATIONS
        self._language_implementations = language_implementations

        if not languages:
            languages = self._language_implementations.keys()
        self._languages = languages

        self._patterns_actions = {}
        for language in languages:
            self._add_language_implementation(language_implementations[language.lower()])

    def _add_language_implementation(self, language_implementation):
        extensions_patterns_actions = language_implementation().get_extensions_patterns_actions()
        if extensions_patterns_actions:
            if isinstance(extensions_patterns_actions, Iterable):
                for extension_pattern_action in extensions_patterns_actions:
                    self._add_extension_pattern_action(extension_pattern_action)
            else:
                self._add_extension_pattern_action(extensions_patterns_actions)

    def _add_extension_pattern_action(self, extension_pattern_action):
        extension = extension_pattern_action.get_extension()
        pattern = extension_pattern_action.get_pattern()
        action = extension_pattern_action.get_action()

        if extension not in self._patterns_actions:
            self._patterns_actions[extension] = [(pattern, action)]
        else:
            self._patterns_actions[extension] += (pattern, action)

    def get_extensions(self):
        return self._patterns_actions.keys()