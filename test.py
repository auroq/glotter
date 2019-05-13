import os
import sys
import pytest

from samplerunner.source import get_sources
from samplerunner.project import get_project_type_by_name


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


def _run_all():
    pytest.main()


def _run_language(language):
    sources_by_type = get_sources(path=os.path.join('archive', language[0], language))
    if all([len(sources) <= 0 for _, sources in sources_by_type.items()]):
        _error_and_exit(f'No valid sources found for language: "{language}"')
    for project_type, sources in sources_by_type.items():
        for source in sources:
            params = _prompt_params(project_type)
            _build_and_run(source, params)


def _run_project(project):
    sources_by_type = get_sources('archive')
    project_type = get_project_type_by_name(project, case_insensitive=True)
    if project_type is None or project_type not in sources_by_type:
        _error_and_exit(f'No valid sources found for project: "{project}"')
    sources = sources_by_type[project_type]
    params = _prompt_params(project_type)
    for source in sources:
        _build_and_run(source, params)


def _run_source(source):
    sources_by_type = get_sources('archive')
    for project_type, sources in sources_by_type.items():
        for src in sources:
            if f'{src.name}{src.extension}'.lower() == source.lower():
                params = _prompt_params(project_type)
                _build_and_run(src, params)
                break
        else:  # If didn't break inner loop continue
            continue
        break  # Else break this loop as well
    else:
        _error_and_exit(f'Source "{source}" could not be found')


