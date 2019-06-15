import re
import os
import sys
import pytest

from glotter.source import get_sources
from glotter.settings import Settings


def test(args):
    if args.language:
        _run_language(args.language)
    elif args.project:
        _run_project(args.project)
    elif args.source:
        _run_source(args.source)
    else:
        _run_all()


def _error_and_exit(msg):
    print(msg)
    sys.exit(1)


def _get_tests(project_type, all_tests, src=None):
    test_function = Settings().get_test_mapping_name(project_type)
    if src is not None:
        filename = f'{src.name}{src.extension}'
        pattern = rf'^(\w/?)*\.py::{test_function}\[{filename}.*\]$'
    else:
        pattern = rf'^(\w/?)*\.py::{test_function}\[.+\]$'
    return [tst for tst in all_tests if re.fullmatch(pattern, tst) is not None]


def _run_all():
    _run_pytest_and_exit()


def _run_language(language):
    all_tests = _collect_tests()
    sources_by_type = get_sources(path=os.path.join('archive', language[0], language))
    if all([len(sources) <= 0 for _, sources in sources_by_type.items()]):
        _error_and_exit(f'No valid sources found for language: "{language}"')
    tests = []
    for project_type, sources in sources_by_type.items():
        for src in sources:
            tests += _get_tests(project_type, all_tests, src)
    _run_pytest_and_exit(*tests)


def _run_project(project):
    try:
        project_type = Settings().get_project_type_by_name(project)
        tests = _get_tests(project_type, _collect_tests())
        _run_pytest_and_exit(*tests)
    except KeyError:
        _error_and_exit(f'No valid sources found for project: "{project}"')


def _run_source(source):
    all_tests = _collect_tests()
    sources_by_type = get_sources('archive')
    for project_type, sources in sources_by_type.items():
        for src in sources:
            filename = f'{src.name}{src.extension}'
            if filename.lower() == source.lower():
                tests = _get_tests(project_type, all_tests, src)
                _run_pytest_and_exit(*tests)
                break
        else:  # If didn't break inner loop continue
            continue
        break  # Else break this loop as well
    else:
        _error_and_exit(f'Source "{source}" could not be found')


def _run_pytest_and_exit(*args):
    args = ['-v'] + list(args)
    code = pytest.main(args=args)
    sys.exit(code)


class TestCollectionPlugin:
    def __init__(self):
        self.collected = []

    def pytest_collection_modifyitems(self, items):
        for item in items:
            self.collected.append(item.nodeid)


def _collect_tests():
    print('============================= collect test totals ==============================')
    plugin = TestCollectionPlugin()
    pytest.main(['-qq', '--collect-only'], plugins=[plugin])
    return plugin.collected

