import os
import pytest

from glotter.source import Source
from glotter.testinfo import TestInfo
from test.mockdocker import Container
from test.fixtures import test_info_string_no_build, test_info_string_with_build, factory, docker, no_io, source_no_build, source_with_build


def test_full_path(test_info_string_no_build):
    src = Source('name', os.path.join('this', 'is', 'a', 'path'), test_info_string_no_build)
    expected = os.path.join('this', 'is', 'a', 'path', 'name')
    actual = src.full_path
    assert actual == expected


@pytest.mark.parametrize(('name', 'expected'), [
    ('name', 'name'),
    ('name.ext', 'name'),
    ('name.name2.ext', 'name.name2')
])
def test_name(name, expected, test_info_string_no_build):
    src = Source(name, os.path.join('this', 'is', 'a', 'path'), test_info_string_no_build)
    actual = src.name
    assert actual == expected


@pytest.mark.parametrize(('name', 'expected'), [
    ('name', ''),
    ('name.ext', '.ext'),
    ('name.name2.ext', '.ext')
])
def test_name(name, expected, test_info_string_no_build):
    src = Source(name, os.path.join('this', 'is', 'a', 'path'), test_info_string_no_build)
    actual = src.extension
    assert actual == expected


def test_test_info_matches_test_info_string(test_info_string_no_build):
    src = Source('name', os.path.join('this', 'is', 'a', 'path'), test_info_string_no_build)
    expected = TestInfo.from_string(test_info_string_no_build, src)
    actual = src.test_info
    assert actual == expected


def test_build_does_nothing_when_build_is_empty(test_info_string_no_build, monkeypatch):
    monkeypatch.setattr('glotter.containerfactory.ContainerFactory.get_container',
                        lambda *args, **kwargs: pytest.fail('get_container was called'))
    src = Source('name', os.path.join('this', 'is', 'a', 'path'), test_info_string_no_build)
    src.build()


def test_build_runs_build_command(factory, source_with_build, monkeypatch, no_io):
    source_with_build.build()
    build_cmd = source_with_build.test_info.container_info.build.strip()
    container = factory.get_container(source_with_build)
    actual = container.execs[0]
    assert actual.cmd.strip() == build_cmd.strip()
    assert not actual['detach']
    assert actual['workdir'] == '/src'


def test_build_raises_error_on_non_zero_exit_code_from_exec(source_with_build, monkeypatch, no_io):
    monkeypatch.setattr('glotter.source.Source._container_exec',
                        lambda *args, **kwargs: (1, 'error message'.encode('utf-8')))
    with pytest.raises(RuntimeError):
        source_with_build.build()
