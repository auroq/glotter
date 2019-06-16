import functools
from enum import Enum

import pytest

from glotter import Settings
from glotter.source import get_sources


def projects_enum(cls):
    settings = Settings()
    if not issubclass(cls, Enum):
        raise AttributeError('projects_enum must be called on a subclass of enum.Enum')
    settings.set_projects_enum(cls)
    return cls


def project_test(project_type):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(func):
            Settings().add_test_mapping(project_type, func)
            return func
        return wrapper
    return decorator


def project_fixture(project_type):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(func):
            sources = get_sources(Settings().source_root).get(project_type)
            return pytest.fixture(
                scope='module',
                params=sources,
                ids=[source.name + source.extension for source in sources],
            )
        return wrapper
    return decorator