import pytest

from glotter.testinfo import ContainerInfo
from glotter import containerfactory


class Containers:
    def __init__(self):
        self.container_list = {}

    def run(self, image, **kwargs):
        if image not in self.container_list:
            self.container_list[image] = []
        self.container_list[image].append(**kwargs)


class Images:
    def __init__(self):
        self.image_list = []

    def add_image(self, name):
        if name not in self.image_list:
            self.image_list.append(name)

    def list(self, name=None, **kwargs):
        if name and name in self.image_list:
            return name

        return self.image_list


class DockerApi:
    def __init__(self, images):
        self.images = images

    def pull(self, repository, **kwargs):
        tag = kwargs.get('tag') or 'latest'
        self.images.add_image(f'{repository}:{tag}')
        return self.images.list(f'{repository}:{tag}')


class DockerMock:
    containers = Containers()
    images = Images()
    api = DockerApi(images)


@pytest.fixture
def docker():
    return DockerMock()


@pytest.fixture
def factory(docker):
    return containerfactory.ContainerFactory(docker_client=docker)


def test_get_image_downloads_image_when_not_found(factory):
    container_info = ContainerInfo(
        image='image',
        tag='tag',
        cmd='cmd',
    )
    factory.get_image(container_info, quiet=True)
    assert f'{container_info.image}:{container_info.tag}' in factory._client.images.image_list
