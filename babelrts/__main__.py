import babelrts

from argparse import ArgumentParser
from os.path import relpath, normpath

def parse_args():
    description = 'BabelRTS v{}. BabelRTS is a regression test selection tool. Given a codebase that has changed, BabelRTS selects modification traversing tests. Find out more at https://github.com/GabrieleMaurina/BabelRTS'.format(babelrts.__version__)
    parser = ArgumentParser(prog= 'python -m babelrts', description=description)
    parser.add_argument('-p', metavar='<project folder>', default='.', help='set project folder (default cwd)')
    parser.add_argument('-s', metavar='<source folder>', nargs='+', default=[''], help='select source folders (default <project folder>)')
    parser.add_argument('-t', metavar='<test folder>', nargs='+', default=[''], help='select test folders (default <project folder>)')
    parser.add_argument('-e', metavar='<excluded>', nargs='+', default=[''], help='exclude files or folders')
    parser.add_argument('-l', metavar='<languages>', nargs='+', help='select target languages (default all)')
    parser.add_argument('-a', action='store_true', help='select all tests')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    project_folder = args.p
    source_folders = {normpath(relpath(source_folder, project_folder)) for source_folder in args.s}
    test_folders = {normpath(relpath(test_folder, project_folder)) for test_folder in args.t}
    selected_tests = babelrts.BabelRTS(args.p, source_folders, test_folders, args.e, args.l).rts(args.a)
    for test_file in selected_tests:
        print(test_file)

if __name__ == '__main__':
    main()