from uuid import uuid4 as uuid

import pytest

from glotter import containerfactory
from glotter.source import Source
from glotter.testinfo import ContainerInfo
from test.mockdocker import DockerMock


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
def test_info_string():
    return """folder:
  extension: ".py"
  naming: "underscore"

container:
  image: "python"
  tag: "3.7-alpine"
  cmd: "python {{ source.name }}{{ source.extension }}"
"""


@pytest.fixture
def source(test_info_string):
    iid = uuid().hex
    return Source(
        name=f'sourcename_{iid}',
        path=f'sourcepath_{iid}',
        test_info_string=test_info_string,
    )