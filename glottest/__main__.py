import sys
import argparse

from glottest.run import run
from glottest.test import test
from glottest.download import download


def main():
    parser = argparse.ArgumentParser(
        prog='glottest',
        usage='''usage: glottest [-h] COMMAND

Commands:
  run         Run sources or group of sources. Use `glottest run --help` for more information.
  test        Run tests for sources or a group of sources. Use `glottest test --help` for more information.
  download    Download all the docker images required to run the tests
'''
    )
    parser.add_argument(
        'command',
        type=str,
        help='Subcommand to run',
        choices=['run', 'test', 'download']
    )
    args = parser.parse_args(sys.argv[1:2])
    commands = {
        'download': parse_download,
        'run': parse_run,
        'test': parse_test,
    }
    commands[args.command]()


def parse_download():
    parser = argparse.ArgumentParser(
        prog='glottest',
        description='Run a source or a group of sources. This command can run a language, a project'
                    'or a single source. Only one option may be specified.',
    )
    args = _parse_args_for_verb(parser)
    download(args)


def parse_run():
    parser = argparse.ArgumentParser(
        prog='glottest',
        description='Run a source or a group of sources. This command can run a language, a project'
                    'or a single source. Only one option may be specified.',
    )
    args = _parse_args_for_verb(parser)
    run(args)


def parse_test():
    parser = argparse.ArgumentParser(
        prog='glottest',
        description='Test a source or a group of sources. This command can test a language, a project'
                    'or a single source. Only one option may be specified.',
    )
    args = _parse_args_for_verb(parser)
    test(args)


def _parse_args_for_verb(parser):
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-s', '--source',
        metavar='SOURCE.EXT',
        type=str,
        help='source filename (not path) to run',
    )
    group.add_argument(
        '-p', '--project',
        metavar='PROJECT',
        type=str,
        help='project to run',
    )
    group.add_argument(
        '-l', '--language',
        metavar='LANGUAGE',
        type=str,
        help='language to run',
    )
    args = parser.parse_args(sys.argv[2:])
    return args


if __name__ == '__main__':
    main()
