import pytest
import functools

from glotter import Settings
from glotter.source import get_sources


def project_test(project_type):
    def decorator(func):
        Settings().add_test_mapping(project_type, func)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator


def project_fixture(project_type):
    sources = get_sources(Settings().source_root).get(project_type)
    return pytest.fixture(
        scope='module',
        params=sources,
        ids=[source.name + source.extension for source in sources],
    )
