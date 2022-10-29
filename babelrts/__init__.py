import babelrts.components

class BabelRTS:

    def __init__(self, project_folder='.', source_folders=None, test_folders=None, excluded=None, languages=None, language_implementations=None):
        self._project_folder = project_folder
        self._source_folders = source_folders
        self._test_folders = test_folders
        self._excluded = excluded
        self._change_discoverer = babelrts.components.change_discoverer.ChangeDiscoverer(self)
        self._dependency_extractor = babelrts.components.dependency_extractor.DependencyExtractor(self, languages, language_implementations)
        self._test_selector = babelrts.components.test_selector.TestSelector(self)

    def rts(self):
        self.get_change_discoverer().explore_codebase()
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