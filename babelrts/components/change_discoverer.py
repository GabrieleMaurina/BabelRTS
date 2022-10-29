from os import walk
from os.path import join
from json import load, dump
from hashlib import sha1

BABELRTS_FILE = '.babelrts'

class ChangeDiscoverer:

    def __init__(self, babelrts):
        self._babelrts = babelrts
        self._all_files = None
        self._source_files = None
        self._test_files = None
        self._changed_files = None

    def explore_codebase(self):
        self._test_files = {file for test_folder in test_folders for file in self._find_files(test_folder)}
        self._source_files = self.get_test_files() - {file for source_folder in source_folders for file in self._find_files(source_folder)}
        self._all_files = self.get_test_files() + self.get_source_files()

        old_hashcodes = _self._load_hashcodes()
        new_hashcodes = {file:self._sha1(file) for file in all_files}
        self._save_hashcodes(new_hashcodes)
        self._changed_files = {file for file, hash in new_hashcodes.items() if file not in old_hashcodes or new_hashcodes[file] != old_hashcodes[file]}

        return self.get_all_files(), self.get_source_files(), self.get_test_files(), self.get_changed_files()

    def _find_files(self, path):
        project_folder = self.get_babelrts().get_project_folder()
        excluded = self.get_babelrts().get_excluded()
        extensions = self.get_babelrts().get_dependency_extractor().get_extensions()

        for root, dirs, files in walk(join(project_folder, path)):
            dirs[:] = [dir for dir in dirs if dir[0] != '.' and dir not in exclude]
            for file in files:
                if file not in exclude:
                    file_path = relpath(join(root, file), project_folder)
                    split = file.rsplit('.', 1)
                    if len(split) == 2:
                        name, extension = split
                        if name and extension and extension in extensions:
                            yield file_path

    def _load_hashcodes(self):
        project_folder = self.get_babelrts().get_project_folder()
        try:
            with open(join(project_folder, BABELRTS_FILE), 'r') as hashcodes:
                return load(hashcodes)
        except Exception:
            return {}


    def _sha1(self, path):
        project_folder = self.get_babelrts().get_project_folder()
        with open(join(project_folder, path), 'rb') as file:
            return sha1(file.read()).hexdigest()

    def _save_hashcodes(self, hashcodes):
        project_folder = self.get_babelrts().get_project_folder()
        with open(join(project_folder, BABELRTS_FILE), 'w') as file:
            dump(hashcodes, file, indent=4, sort_keys=True)

    def get_all_files(self):
        return self._all_files

    def get_source_files(self):
        return self._source_files

    def get_test_files(self):
        return self._test_files

    def get_changed_files(self):
        return self._changed_files

    def get_babelrts(self):
        return self._babelrts

    def set_babelrts(self, babelrts):
        self._babelrts = babelrts