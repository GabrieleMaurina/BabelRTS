from collections import deque

class TestSelector:

    def __init__(self, babelrts):
        self.set_babelrts(babelrts)
        self._selected_tests = None
    
    def select_tests(self):
        test_files = self.get_babelrts().get_change_discoverer().get_test_files()
        changed_files = self.get_babelrts().get_change_discoverer().get_changed_files()
        dependency_graph = self.get_babelrts().get_dependency_extractor().get_dependency_graph()
        self._selected_tests = {test_file for test_file in test_files if self._dfs_changed(test_file, changed_files, dependency_graph)}
        return self._selected_tests

    def _dfs_changed(self, test_file, changed_files, dependency_graph):
        files = deque((test_file,))
        visited = set()
        while files:
            file = files.pop()
            if file not in visited:
                visited.add(file)
                if file in changed_files:
                    return True
                elif file in dependency_graph:
                    files.extend(dependency_graph[file])
        return False

    def get_selected_tests(self):
        return self._selected_tests

    def get_babelrts(self):
        return self._babelrts

    def set_babelrts(self, babelrts):
        self._babelrts = babelrts