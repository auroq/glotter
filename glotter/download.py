import os
import sys

from glotter.source import get_sources
from glotter.settings import Settings
from glotter.containerfactory import ContainerFactory


def download(args):
    if args.language:
        _download_language(args.language)
    elif args.project:
        _download_project(args.project)
    elif args.source:
        _download_source(args.source)
    else:
        _download_all()


def _download_image_from_source(source):
    ContainerFactory().get_image(source.test_info.container_info)


def _error_and_exit(msg):
    print(msg)
    sys.exit(1)


def _download_all():
    sources_by_type = get_sources(Settings().source_root)
    for _, sources in sources_by_type.items():
        for source in sources:
            _download_image_from_source(source)


def _download_language(language):
    sources_by_type = get_sources(path=os.path.join(Settings().source_root, language[0], language))
    if all([len(sources) <= 0 for _, sources in sources_by_type.items()]):
        _error_and_exit(f'No valid sources found for language: "{language}"')
    for project_type, sources in sources_by_type.items():
        for source in sources:
            _download_image_from_source(source)


def _download_project(project):
    sources_by_type = get_sources(Settings().source_root)
    try:
        project_type = Settings().verify_project_type(project)
        sources = sources_by_type[project_type]
        for source in sources:
            _download_image_from_source(source)
    except KeyError:
        _error_and_exit(f'No valid sources found for project: "{project}"')


def _download_source(source):
    sources_by_type = get_sources(Settings.source_root)
    for project_type, sources in sources_by_type.items():
        for src in sources:
            if f'{src.name}{src.extension}'.lower() == source.lower():
                _download_image_from_source(src)
                break
        else:  # If didn't break inner loop continue
            continue
        break  # Else break this loop as well
    else:
        _error_and_exit(f'Source "{source}" could not be found')
