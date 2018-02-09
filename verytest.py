from itertools import groupby
import argparse
import pathlib
import re
import subprocess

root_path = '.'
compiler = 'iverilog'
executor = 'vvp'


def run():
    print("Searching in root:", root_path)

    path = pathlib.Path(root_path)

    def key(x): return x.parent
    files_group = groupby(sorted([x for x in path.rglob(
        '*.v') if not re.match('(\w|\d)+\.test\.v', x.name)], key=key), key=key)

    for parent_dir, files in files_group:
        print('Runnint tests in:', parent_dir)
        current_dir = pathlib.Path(parent_dir)

        for filename in files:
            test_file_name = current_dir.with_name(filename.stem + '.test.v')

            print('Run test for...', filename.name)

            testing_dir = str(filename.parent)

            objectfile_name = filename.stem
            compile_process = subprocess.Popen(
                [compiler,
                 '-o{}'.format(objectfile_name),
                 filename.name,
                 test_file_name.name],
                cwd=testing_dir,
            )
            compile_process.wait()

            test_run_process = subprocess.Popen(
                [executor,
                 objectfile_name],
                cwd=testing_dir,
            )
            test_run_process.wait()


class SetRoot(argparse.Action):

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(SetRoot, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, optios_string=None):
        global root_path
        root_path = values


args_parser = argparse.ArgumentParser()
args_parser.add_argument(
    '--root', help='Project\'s root direcory', default='.', action=SetRoot)

if __name__ == '__main__':
    root = args_parser.parse_args()
    run()
