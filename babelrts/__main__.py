import babelrts

from argparse import ArgumentParser
from os.path import relpath

def parse_args():
    description = 'BabelRTS v{}. BabelRTS is a regression test selection tool. Given a codebase that has changed, BabelRTS selects modification traversing tests. Find out more at https://github.com/GabrieleMaurina/BabelRTS'.format(babelrts.__version__)
    parser = ArgumentParser(prog= 'python -m babelrts', description=description)
    parser.add_argument('-p', metavar='<project folder>', default='', help='set project folder (default cwd)')
    parser.add_argument('-s', metavar='<source folder>', nargs='+', default=[''], help='select source folders (default <project folder>)')
    parser.add_argument('-t', metavar='<test folder>', nargs='+', default=[''], help='select test folders (default <project folder>)')
    parser.add_argument('-e', metavar='<excluded>', nargs='+', default=[''], help='exclude files or folders')
    parser.add_argument('-l', metavar='<languages>', nargs='+', help='select target languages (default all)')
    parser.add_argument('-a', action='store_true', help='select all tests')
    parser.add_argument('-g', metavar='<graph path>', nargs='?', default='', help='generate graph')
    parser.add_argument('--git', metavar='<commit>', nargs='?', default='', help='use git diff to determine changes')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    project_folder = args.p
    source_folders = {relpath(source_folder, project_folder) if project_folder and source_folder else source_folder for source_folder in args.s}
    test_folders = {relpath(test_folder, project_folder) if project_folder and test_folder else test_folder for test_folder in args.t}
    if args.git == None:
        args.git = ''
    elif args.git == '':
        args.git = None
    babelRTS = babelrts.BabelRTS(project_folder, source_folders, test_folders, args.e, args.l, git=args.git)
    selected_tests = babelRTS.rts(args.a)
    for test_file in selected_tests:
        print(test_file)
    if args.g is None:
        babelRTS.get_dependency_extractor().visualize_digraph()
    elif args.g:
        if '.' in args.g:
            name, extension = args.g.rsplit('.', 1)
            if name and extension:
                babelRTS.get_dependency_extractor().visualize_digraph(filename=name, format=extension)
            else:
                babelRTS.get_dependency_extractor().visualize_digraph(filename=args.g)
        else:
            babelRTS.get_dependency_extractor().visualize_digraph(filename=args.g)

if __name__ == '__main__':
    main()
