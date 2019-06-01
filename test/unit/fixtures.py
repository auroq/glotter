from uuid import uuid4 as uuid

import pytest

from glotter import containerfactory
from glotter.source import Source
from glotter.testinfo import ContainerInfo
from test.unit.mockdocker import DockerMock


@pytest.fixture
def docker():
    docker_mock = DockerMock()
    yield docker_mock
    docker_mock.clear()


@pytest.fixture
def factory(docker):
    return containerfactory.ContainerFactory(docker_client=docker)


@pytest.fixture
def container_info():
    iid = uuid().hex
    return ContainerInfo(
        image=f'image_{iid}',
        tag=f'tag_{iid}',
        cmd=f'cmd_{iid}',
    )


@pytest.fixture
def test_info_string_no_build():
    return """folder:
  extension: ".py"
  naming: "underscore"

container:
  image: "python"
  tag: "3.7-alpine"
  cmd: "python {{ source.name }}{{ source.extension }}"
"""


@pytest.fixture
def test_info_string_with_build():
    return """folder:
  extension: ".go"
  naming: "hyphen"

container:
  image: "golang"
  tag: "1.12-alpine"
  build: "go build -o {{ source.name }} {{ source.name}}{{ source.extension }}"
  cmd: "./{{ source.name }}"
"""


@pytest.fixture
def source_no_build(test_info_string_no_build):
    iid = uuid().hex
    return Source(
        name=f'sourcename_{iid}',
        path=f'sourcepath_{iid}',
        test_info_string=test_info_string_no_build,
    )


@pytest.fixture
def source_with_build(test_info_string_with_build):
    iid = uuid().hex
    return Source(
        name=f'sourcename_{iid}',
        path=f'sourcepath_{iid}',
        test_info_string=test_info_string_with_build,
    )


@pytest.fixture
def no_io(monkeypatch):
    monkeypatch.setattr('tempfile.mkdtemp', lambda *args, **kwargs: 'TEMP_DIR')
    monkeypatch.setattr('shutil.copy', lambda *args, **kwargs: '')
    monkeypatch.setattr('shutil.rmtree', lambda *args, **kwargs: '')
