from glob import iglob
from os import walk
from os.path import join
from json import load, dump
from hashlib import sha1
from os.path import relpath, normpath, isfile, isdir, basename, splitext
from os import remove
from subprocess import run

BABELRTS_FILE = '.babelrts'


class ChangeDiscoverer:

    def __init__(self, babelrts):
        self.set_babelrts(babelrts)
        self._all_files = None
        self._source_files = None
        self._test_files = None
        self._changed_files = None

    def explore_codebase(self):
        self._init_excluded()
        self._init_test_files()
        self._init_source_files()
        self._check_test_regexp()

        self.set_all_files(self.get_test_files() | self.get_source_files())

        commit = self.get_babelrts().get_commit()
        if commit is None:
            old_hashcodes = self._load_hashcodes()
            new_hashcodes = {file: self._sha1(file)
                             for file in self.get_all_files()}
            self._save_hashcodes(new_hashcodes)
            self.set_changed_files({file for file, hash in new_hashcodes.items(
            ) if file not in old_hashcodes or new_hashcodes[file] != old_hashcodes[file]})
        else:
            changed_files = self._git_diff(commit)
            self.set_changed_files(changed_files)

        return self.get_all_files(), self.get_source_files(), self.get_test_files(), self.get_changed_files()

    def _git_diff(self, commit):
        if not commit:
            commit = 'HEAD~1'
        cmd = f'git --no-pager diff --name-only {commit}'
        cwd = self.get_babelrts().get_project_folder()
        result = run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)
        if result.returncode:
            raise Exception(result.stderr)
        extensions = self.get_babelrts().get_dependency_extractor().get_extensions()
        files = {normpath(file) for file in result.stdout.split(
            '\n') if file and splitext(file)[1][1:] in extensions}
        return files

    def _find_files(self, path):
        project_folder = self.get_babelrts().get_project_folder()
        extensions = self.get_babelrts().get_dependency_extractor().get_extensions()
        for path in iglob(join(project_folder, path), recursive=True):
            if isfile(path):
                if self._is_excluded_file(path):
                    continue
                file_path = normpath(relpath(path, project_folder))
                file_name = basename(file_path)
                name, extension = splitext(file_name)
                if name and extension and extension[1:] in extensions:
                    yield file_path
            elif isdir(path):
                if self._is_excluded_folder(path):
                    continue
                for root, dirs, files in walk(path):
                    dirs[:] = [dir for dir in dirs if not dir.startswith('.')]
                    for file in files:
                        file_path = normpath(
                            relpath(join(root, file), project_folder))
                        if self._is_excluded_file(file_path):
                            continue
                        name, extension = splitext(file)
                        if name and extension and extension[1:] in extensions:
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

    def clear_hashcodes(self):
        project_folder = self.get_babelrts().get_project_folder()
        hashcode_file = join(project_folder, BABELRTS_FILE)
        if isfile(hashcode_file):
            remove(hashcode_file)

    def _init_excluded(self):
        excluded_files = set()
        excluded_folders = set()
        project_folder = self.get_babelrts().get_project_folder()
        for excluded in self.get_babelrts().get_excluded():
            for path in iglob(join(project_folder, excluded), recursive=True):
                if isfile(path):
                    excluded_files.add(normpath(relpath(path, project_folder)))
                elif isdir(path):
                    excluded_folders.add(
                        normpath(relpath(path, project_folder)))
        self.set_excluded_files(excluded_files)
        self.set_excluded_folders(excluded_folders)

    def get_excluded_files(self):
        return self._excluded_files

    def set_excluded_files(self, excluded_files):
        self._excluded_files = excluded_files

    def get_excluded_folders(self):
        return self._excluded_folders

    def set_excluded_folders(self, excluded_folders):
        self._excluded_folders = excluded_folders

    def _is_excluded_file(self, path):
        return path in self.get_excluded_files() or any(path.startswith(folder) for folder in self.get_excluded_folders())

    def _is_excluded_folder(self, path):
        return path in self.get_excluded_folders() or any(path.startswith(folder) for folder in self.get_excluded_folders())

    def get_all_files(self):
        return self._all_files

    def set_all_files(self, all_files):
        self._all_files = all_files

    def _init_source_files(self):
        source_files = set()
        for source in self.get_babelrts().get_sources():
            for file in self._find_files(source):
                source_files.add(file)
        self.set_source_files(source_files - self.get_test_files())

    def get_source_files(self):
        return self._source_files

    def set_source_files(self, source_files):
        self._source_files = source_files

    def _init_test_files(self):
        test_files = set()
        for test in self.get_babelrts().get_tests():
            for file in self._find_files(test):
                test_files.add(file)
        self.set_test_files(test_files)

    def get_test_files(self):
        return self._test_files

    def set_test_files(self, test_files):
        self._test_files = test_files

    def _check_test_regexp(self):
        test_regexp = self.get_babelrts().get_test_regexp()
        if test_regexp is not None:
            not_tests = []
            for test in self.get_test_files():
                if not test_regexp.match(test):
                    not_tests.append(test)
            for not_test in not_tests:
                self.get_test_files().remove(not_test)
                self.get_source_files().add(not_test)

    def get_changed_files(self):
        return self._changed_files

    def set_changed_files(self, changed_files):
        self._changed_files = changed_files

    def get_babelrts(self):
        return self._babelrts

    def set_babelrts(self, babelrts):
        self._babelrts = babelrts
