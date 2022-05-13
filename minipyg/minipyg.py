import argparse
import subprocess
import sys
import json


def install_package(package, version):
    print('Installing', package + ', version', version)
    subprocess.run(['python3', '-m', 'pip', 'install', package + '==' + version])
    print('Complete')


def delete_package(package):
    print('Uninstalling', package)
    subprocess.run(['python3', '-m', 'pip', 'uninstall', package, '-y'])
    print('Complete')


def entry():
    parser = argparse.ArgumentParser(prog='minipyg')
    parser.add_argument('command')

    args = parser.parse_args()

    if args.commend == 'install':
        pass

    if args.command == 'uninstall':
        pass

    if args.command in ('update', 'run'):

        if sys.prefix != sys.base_prefix:
            pr = subprocess.run(['pip', 'freeze'], stdout=subprocess.PIPE)
            actual_deps = list(
                map(
                    lambda x: x.decode('utf-8'),
                    filter(
                        lambda x: len(x) > 0,
                        pr.stdout.split(b'\n')
                    )
                )
            )

            actual_deps_dict = {}

            for dep in actual_deps:
                _d = dep.split('==')
                if _d[0] != 'minipyg':
                    actual_deps_dict[_d[0]] = _d[1]

            incoming_deps_dict = {}

            with open('requirements.txt') as f:
                for line in f.readlines():
                    _d = line.split('==')
                    if _d[0] != 'minipyg':
                        incoming_deps_dict[_d[0]] = _d[1]

            # checking package addition/changing
            for item in incoming_deps_dict:
                # changing
                if item in actual_deps_dict:
                    if incoming_deps_dict[item] != actual_deps_dict[item]:
                        delete_package(item)
                        install_package(item, incoming_deps_dict[item])

                # addition
                else:
                    install_package(item, incoming_deps_dict[item])

            # checking deletion
            for item in actual_deps_dict:
                if item not in incoming_deps_dict:
                    if item != 'minipyg':
                        delete_package(item)

        else:
            print('You are outside of the venv. Please activate it via `source venv/bin/activate` command.')

    if args.command == 'run':
        with open('minipyg.json') as f:
            d = json.load(f)
            if 'run' in d:
                subprocess.run(d['run'].split())
