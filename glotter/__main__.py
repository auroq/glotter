import sys
import argparse

from glotter.run import run
from glotter.test import test
from glotter.download import download
from glotter.report import report


def main():
    parser = argparse.ArgumentParser(
        prog='glotter',
        usage='''usage: glotter [-h] COMMAND

Commands:
  run         Run sources or group of sources. Use `glotter run --help` for more information.
  test        Run tests for sources or a group of sources. Use `glotter test --help` for more information.
  download    Download all the docker images required to run the tests
  report      Output a report of discovered sources for configured projects and languages
'''
    )
    parser.add_argument(
        'command',
        type=str,
        help='Subcommand to run',
        choices=['run', 'test', 'download', 'report']
    )
    args = parser.parse_args(sys.argv[1:2])
    commands = {
        'download': parse_download,
        'run': parse_run,
        'test': parse_test,
        'report': parse_report,
    }
    commands[args.command]()


def parse_download():
    parser = argparse.ArgumentParser(
        prog='glotter',
        description='Download images for a source or a group of sources. This command can be filtered by language, '
                    'project, or a single source. Only one option may be specified.',
    )
    args = _parse_args_for_verb(parser)
    download(args)


def parse_run():
    parser = argparse.ArgumentParser(
        prog='glotter',
        description='Run a source or a group of sources. This command can be filtered by language, project'
                    'or a single source. Only one option may be specified.',
    )
    args = _parse_args_for_verb(parser)
    run(args)


def parse_test():
    parser = argparse.ArgumentParser(
        prog='glotter',
        description='Test a source or a group of sources. This command can be filtered by language, project'
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


def parse_report():
    parser = argparse.ArgumentParser(
        prog='glotter',
        description='Output a report of discovered sources for configured projects and languages'
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-o', '--output',
        metavar='REPORT_PATH',
        type=str,
        help='output the report as a csv at REPORT_PATH instead of to stdout',
    )
    args = parser.parse_args(sys.argv[2:])
    report(args)


if __name__ == '__main__':
    main()
