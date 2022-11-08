from babelrts import BabelRTS

import pytest
from os.path import isdir, join
from os import makedirs
from subprocess import run

PATH = 'repos'

REPOS = (
    'https://github.com/apache/commons-cli.git',
    'https://github.com/dmlc/minerva.git',
    'https://github.com/paramiko/paramiko.git',
    'https://github.com/vega/datalib.git',
    'https://github.com/erlydtl/erlydtl.git',
)

TEST_INPUTS = (
    ('repos/commons-cli', 'src/main/java', 'src/test/java', 'java'),
    ('repos/minerva', 'minerva', 'tests', 'c++'),
    ('repos/paramiko', 'paramiko', 'tests', 'python'),
    ('repos/datalib', 'src', 'test', 'javascript'),
    ('repos/erlydtl', 'src', 'test', 'erlang'),
)

@pytest.fixture(scope='module', autouse=True)
def clone_repos():
    makedirs(PATH, exist_ok=True)
    for repo in REPOS:
        name = repo.rsplit('/', 1)[-1][:-4]
        if not isdir(join(PATH, name)):
            run(f'git clone {repo}', shell=True, cwd=PATH)

@pytest.mark.parametrize('project_folder, source_folders, test_folders, languages', TEST_INPUTS)
def test_babelrts(project_folder, source_folders, test_folders, languages):
    babelRTS = BabelRTS(project_folder, source_folders, test_folders, languages=languages)
    babelRTS.get_change_discoverer().clear_babelrts_data()
    selected_tests = babelRTS.rts()
    dependency_graph = babelRTS.get_dependency_extractor().get_dependency_graph()
    assert len(selected_tests) > 0
    assert len(dependency_graph) > 0
    selected_tests = babelRTS.rts()
    dependency_graph = babelRTS.get_dependency_extractor().get_dependency_graph()
    assert len(selected_tests) == 0
    assert len(dependency_graph) > 0