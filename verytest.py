import argparse
import pathlib

root_path = None or '.'


def run():
    print("Searching in:", root_path)

    path = pathlib.Path(root_path)

    for filename in path.rglob('*.v'):
        print(filename)


class SetRoot(argparse.Action):

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(SetRoot, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, optios_string=None):
        global root_path
        root_path = values


args_parser = argparse.ArgumentParser()
args_parser.add_argument('--root', help='Project\'s root direcory', default='.', action=SetRoot)

if __name__ == '__main__':
    root = args_parser.parse_args()
    run()
