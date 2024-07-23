import babelrts.components

from os.path import normpath

__author__ = 'Gabriele Maurina'
__copyright__ = '© 2020-2024 Gabriele Maurina'
__credits__ = ['Gabriele Maurina']
__license__ = 'MIT'
__version__ = '1.2.1'
__maintainer__ = 'Gabriele Maurina'
__email__ = 'gabrielemaurina95@gmail.com'
__status__ = 'Production'


class BabelRTS:

    def __init__(self, project_folder='.', sources=None, tests=None, excluded=(), languages=None, language_implementations=None, commit=None):
        self.set_project_folder(project_folder)
        self.set_sources(sources)
        self.set_tests(tests)
        self.set_excluded(excluded)
        self.set_languages(languages)
        self.set_commit(commit)
        self.set_change_discoverer(
            babelrts.components.change_discoverer.ChangeDiscoverer(self))
        self.set_dependency_extractor(babelrts.components.dependency_extractor.DependencyExtractor(
            self, languages, language_implementations))
        self.set_test_selector(
            babelrts.components.test_selector.TestSelector(self))

    def rts(self, all=False):
        self.get_change_discoverer().explore_codebase()

        if all or self.get_change_discoverer().get_test_files().issubset(self.get_change_discoverer().get_changed_files()):
            self.get_test_selector().set_selected_tests(
                self.get_change_discoverer().get_test_files())
            return self.get_test_selector().get_selected_tests()

        if self.get_change_discoverer().get_changed_files():
            self.get_dependency_extractor().generate_dependency_graph()
            return self.get_test_selector().select_tests()

        return ()

    def get_project_folder(self):
        return self._project_folder

    def set_project_folder(self, project_folder):
        self._project_folder = normpath(project_folder)

    def get_sources(self):
        return self._sources

    def set_sources(self, sources):
        if not sources:
            self._sources = ('',)
        elif isinstance(sources, str):
            self._sources = (normpath(sources),)
        else:
            self._sources = tuple(normpath(source) for source in sources)

    def get_tests(self):
        return self._tests

    def set_tests(self, tests):
        if not tests:
            self._tests = ('',)
        elif isinstance(tests, str):
            self._tests = (normpath(tests),)
        else:
            self._tests = tuple(normpath(test) for test in tests)

    def get_excluded(self):
        return self._excluded

    def set_excluded(self, excluded):
        if not excluded:
            self._excluded = ()
        elif isinstance(excluded, str):
            self._excluded = (normpath(excluded),)
        else:
            self._excluded = tuple(normpath(path) for path in excluded)

    def get_languages(self):
        return self._languages

    def set_languages(self, languages):
        if not languages:
            self._languages = ()
        elif isinstance(languages, str):
            self._languages = (languages.lower(),)
        else:
            self._languages = tuple(language.lower() for language in languages)

    def set_commit(self, commit):
        self._commit = commit

    def get_commit(self):
        return self._commit

    def get_change_discoverer(self):
        return self._change_discoverer

    def set_change_discoverer(self, change_discoverer):
        self._change_discoverer = change_discoverer

    def get_dependency_extractor(self):
        return self._dependency_extractor

    def set_dependency_extractor(self, dependency_extractor):
        self._dependency_extractor = dependency_extractor

    def get_test_selector(self):
        return self._test_selector

    def set_test_selector(self, test_selector):
        self._test_selector = test_selector
