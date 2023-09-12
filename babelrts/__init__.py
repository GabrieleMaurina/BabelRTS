import babelrts.components

from os.path import normpath

__author__ = 'Gabriele Maurina'
__copyright__ = '© 2020-2022 Gabriele Maurina'
__credits__ = ['Gabriele Maurina']
__license__ = 'MIT'
__version__ = '1.2.0'
__maintainer__ = 'Gabriele Maurina'
__email__ = 'gabrielemaurina95@gmail.com'
__status__ = 'Production'

class BabelRTS:

    def __init__(self, project_folder='.', source_folders=None, test_folders=None, excluded=(), languages=None, language_implementations=None, git=None):
        self.set_project_folder(project_folder)
        self.set_source_folders(source_folders)
        self.set_test_folders(test_folders)
        self.set_excluded(excluded)
        self.set_git(git)
        self.set_change_discoverer(babelrts.components.change_discoverer.ChangeDiscoverer(self))
        self.set_dependency_extractor(babelrts.components.dependency_extractor.DependencyExtractor(self, languages, language_implementations))
        self.set_test_selector(babelrts.components.test_selector.TestSelector(self))

    def rts(self, all=False):
        self.get_change_discoverer().explore_codebase()

        if all or self.get_change_discoverer().get_test_files().issubset(self.get_change_discoverer().get_changed_files()):
            self.get_test_selector().set_selected_tests(self.get_change_discoverer().get_test_files())
            return self.get_test_selector().get_selected_tests()

        if self.get_change_discoverer().get_changed_files():
            self.get_dependency_extractor().generate_dependency_graph()
            return self.get_test_selector().select_tests()

        return ()

    def get_project_folder(self):
        return self._project_folder

    def set_project_folder(self, project_folder):
        self._project_folder = normpath(project_folder)

    def get_source_folders(self):
        return self._source_folders

    def set_source_folders(self, source_folders):
        if not source_folders:
            self._source_folders = ('',)
        elif isinstance(source_folders, str):
            self._source_folders = (normpath(source_folders),)
        else:
            self._source_folders = tuple(normpath(source_folder) for source_folder in source_folders)

    def get_test_folders(self):
        return self._test_folders

    def set_test_folders(self, test_folders):
        if not test_folders:
            self._test_folders = ('',)
        elif isinstance(test_folders, str):
            self._test_folders = (normpath(test_folders),)
        else:
            self._test_folders = tuple(normpath(test_folder) for test_folder in test_folders)

    def get_excluded(self):
        return self._excluded

    def set_excluded(self, excluded):
        if not excluded:
            self._excluded = ()
        elif isinstance(excluded, str):
            self._excluded = (normpath(excluded),)
        else:
            self._excluded = tuple(normpath(path) for path in excluded)

    def set_git(self, git):
        self._git = git

    def get_git(self):
        return self._git

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
