import os
import pytest

from glotter.source import Source
from glotter.testinfo import TestInfo
from test.mockdocker import Container
from test.fixtures import test_info_string


def test_full_path(test_info_string):
    src = Source('name', os.path.join('this', 'is', 'a', 'path'), test_info_string)
    expected = os.path.join('this', 'is', 'a', 'path', 'name')
    actual = src.full_path
    assert actual == expected


@pytest.mark.parametrize(('name', 'expected'), [
    ('name', 'name'),
    ('name.ext', 'name'),
    ('name.name2.ext', 'name.name2')
])
def test_name(name, expected, test_info_string):
    src = Source(name, os.path.join('this', 'is', 'a', 'path'), test_info_string)
    actual = src.name
    assert actual == expected


@pytest.mark.parametrize(('name', 'expected'), [
    ('name', ''),
    ('name.ext', '.ext'),
    ('name.name2.ext', '.ext')
])
def test_name(name, expected, test_info_string):
    src = Source(name, os.path.join('this', 'is', 'a', 'path'), test_info_string)
    actual = src.extension
    assert actual == expected


def test_test_info_matches_test_info_string(test_info_string):
    src = Source('name', os.path.join('this', 'is', 'a', 'path'), test_info_string)
    expected = TestInfo.from_string(test_info_string, src)
    actual = src.test_info
    assert actual == expected

# def test_idk(monkeypatch):
#     monkeypatch.setattr('glotter.ContainerFactory.get_container', lambda *args, **kwargs: Container(**kwargs))
