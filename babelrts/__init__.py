import babelrts.components

__author__ = 'Gabriele Maurina'
__copyright__ = '© 2020-2022 Gabriele Maurina'
__credits__ = ['Gabriele Maurina']
__license__ = 'MIT'
__version__ = '1.2.0'
__maintainer__ = 'Gabriele Maurina'
__email__ = 'gabrielemaurina95@gmail.com'
__status__ = 'Production'

class BabelRTS:

    def __init__(self, project_folder='.', source_folders=None, test_folders=None, excluded=(), languages=None, language_implementations=None):
        if not source_folders:
            source_folders = (project_folder,)
        if not test_folders:
            test_folders = (project_folder,)
        self._project_folder = project_folder
        self._source_folders = source_folders
        self._test_folders = test_folders
        self._excluded = excluded
        self._change_discoverer = babelrts.components.change_discoverer.ChangeDiscoverer(self)
        self._dependency_extractor = babelrts.components.dependency_extractor.DependencyExtractor(self, languages, language_implementations)
        self._test_selector = babelrts.components.test_selector.TestSelector(self)

    def rts(self, select_all=False):
        self.get_change_discoverer().explore_codebase()

        if select_all:
            return self.get_change_discoverer().get_test_files()

        self.get_dependency_extractor().generate_dependency_graph()
        self.get_test_selector().select_tests()
        return self.get_test_selector().get_selected_tests()

    def get_project_folder(self):
        return self._project_folder

    def set_project_folder(self, project_folder):
        self._project_folder = project_folder

    def get_source_folders(self):
        return self._source_folders

    def set_source_folders(self, source_folders):
        self._source_folders = source_folders

    def get_test_folders(self):
        return self._test_folders

    def set_project_folder(self, test_folders):
        self._test_folders = test_folders

    def get_excluded(self):
        return self._excluded

    def set_project_folder(self, excluded):
        self._project_folder = excluded