import argparse
import pathlib


class RunTests(argparse.Action):

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(RunTests, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, optios_string=None):
        root = values or '.'
        print("Searching in:", root)

        path = pathlib.Path(root)

        for filename in path.rglob('*.v'):
            print(filename)

args_parser = argparse.ArgumentParser()
args_parser.add_argument('--root', help='Project\'s root direcory', default='.', action=RunTests)

if __name__ == '__main__':
    root = args_parser.parse_args()
