from itertools import groupby
import argparse
import pathlib
import re
import subprocess
import json


root_path = '.'
compiler = 'iverilog'
executor = 'vvp'
output_file = 'test_result.json'


def parse_test_output_line(line):
    parts = line.split(':')
    status = True if parts[1].strip().lower() == 'ok' else False
    name = parts[0].replace('Test ', '').replace('"', '')
    return name, status


def run():
    print("Searching in root:", root_path)

    path = pathlib.Path(root_path)

    output_raw = []

    all_tests_counter = 0
    good_tests_counter = 0

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
                stdout=subprocess.PIPE,
            )
            output = [x for x in test_run_process.stdout.read().decode(
                'utf8').split('\n', ) if x]
            parsed_output = [parse_test_output_line(x) for x in output]

            all_tests_counter += len(parsed_output)
            good_tests_counter += len([x for x in parsed_output if x[1] is True])
            output_raw.append(
                {'module': filename.name, 'tests': [parsed_output]})

            test_run_process.wait()

        total_result = {'summary': {'total': all_tests_counter, 'good': good_tests_counter, 'failed': all_tests_counter -
                                    good_tests_counter, 'it_is_good': all_tests_counter == good_tests_counter}, 'tests': output_raw}

        with open(output_file, 'w', encoding='utf8') as file:
            file.write(json.dumps(total_result))


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
