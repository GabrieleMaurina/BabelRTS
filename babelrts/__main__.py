from babelrts import BabelRTS, __version__

from argparse import ArgumentParser


def parse_args():
    description = f'BabelRTS v{__version__}. BabelRTS is a regression test selection tool. Given a codebase that has changed, BabelRTS selects modification traversing tests. Find out more at https://github.com/GabrieleMaurina/BabelRTS'
    parser = ArgumentParser(prog='python -m babelrts', description=description)
    parser.add_argument('-p', metavar='<project folder>',
                        default='', help='set project folder (default cwd)')
    parser.add_argument('-s', metavar='<source folder>', nargs='+',
                        default=[''], help='select source files or folders (default <project folder>)')
    parser.add_argument('-t', metavar='<test folder>', nargs='+',
                        default=[''], help='select test file or folders (default <project folder>)')
    parser.add_argument('-e', metavar='<excluded>', nargs='+',
                        default=[], help='exclude files or folders')
    parser.add_argument('-l', metavar='<languages>', nargs='+',
                        help='select target languages (default all)')
    parser.add_argument('-a', action='store_true', help='select all tests')
    parser.add_argument('-c', metavar='<commit>', nargs='?',
                        default='', help='use git diff to determine changes since commit')
    parser.add_argument('-g', metavar='<graph path>',
                        nargs='?', default='', help='generate graph')
    args = parser.parse_args()
    if args.c == None:
        args.c = ''
    elif args.c == '':
        args.c = None
    return args


def main():
    args = parse_args()
    babelRTS = BabelRTS(args.p, args.s, args.t, args.e, args.l, args.c)
    selected_tests = babelRTS.rts(args.a)
    for test_file in selected_tests:
        print(test_file)
    if args.g is None:
        babelRTS.get_dependency_extractor().visualize_digraph()
    elif args.g:
        if '.' in args.g:
            name, extension = args.g.rsplit('.', 1)
            if name and extension:
                babelRTS.get_dependency_extractor().visualize_digraph(
                    filename=name, format=extension)
            else:
                babelRTS.get_dependency_extractor().visualize_digraph(filename=args.g)
        else:
            babelRTS.get_dependency_extractor().visualize_digraph(filename=args.g)


if __name__ == '__main__':
    main()
