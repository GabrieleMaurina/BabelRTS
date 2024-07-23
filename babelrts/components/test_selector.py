from collections import deque


class TestSelector:

    def __init__(self, babelrts):
        self.set_babelrts(babelrts)
        self._selected_tests = None

    def select_tests(self):
        test_files = self.get_babelrts().get_change_discoverer().get_test_files()
        changed_files = self.get_babelrts().get_change_discoverer().get_changed_files()
        dependencies = self.get_babelrts().get_dependency_extractor().get_dependencies()

        flipped_graph = {}
        for file, dependencies in dependencies.items():
            for dependency in dependencies:
                if dependency not in flipped_graph:
                    flipped_graph[dependency] = []
                flipped_graph[dependency].append(file)

        self.set_selected_tests(self._dfs_changed(
            test_files, changed_files, flipped_graph))

        return self.get_selected_tests()

    def _dfs_changed(self, test_files, changed_files, dependencies):
        files = deque(changed_files)
        visited = set()
        selected_tests = set()
        while files:
            file = files.pop()
            if file not in visited:
                visited.add(file)
                if file in test_files:
                    selected_tests.add(file)
                if file in dependencies:
                    files.extend(dependencies[file])
        return selected_tests

    def get_selected_tests(self):
        return self._selected_tests

    def set_selected_tests(self, selected_tests):
        self._selected_tests = selected_tests

    def get_babelrts(self):
        return self._babelrts

    def set_babelrts(self, babelrts):
        self._babelrts = babelrts
