from uuid import uuid4 as uuid


class Container:
    def __init__(self, image, name, attributes):
        self.image = image
        self.name = name
        self.attributes = attributes
        self.removed = False

    def __getitem__(self, key):
        return self.attributes[key]

    def remove(self, *args, **kwargs):
        self.removed = True


class Containers:
    container_list = {}

    @classmethod
    def run(cls, image, **kwargs):
        name = kwargs['name'] if 'name' in kwargs else uuid().hex
        info = Container(image, name, kwargs)
        if name not in cls.container_list:
            cls.container_list[name] = info
            return cls.container_list[name]
        raise EnvironmentError('Container exists')

    @classmethod
    def clear(cls):
        cls.container_list = {}


class Images:
    image_list = []

    @classmethod
    def add_image(cls, name):
        if name not in cls.image_list:
            Images.image_list.append(name)

    @classmethod
    def list(cls, name=None, **kwargs):
        if name and name in cls.image_list:
            return [name]

        return cls.image_list

    @classmethod
    def clear(cls):
        cls.image_list = []


class DockerApi:
    @staticmethod
    def pull(repository, **kwargs):
        tag = kwargs.get('tag') or 'latest'
        Images.add_image(f'{repository}:{tag}')
        return Images.list(f'{repository}:{tag}')


class DockerMock:
    containers = Containers
    images = Images
    api = DockerApi

    @classmethod
    def clear(cls):
        cls.images.clear()
        cls.containers.clear()