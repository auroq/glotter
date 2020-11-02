from __future__ import annotations

import yaml
from jinja2 import Environment, BaseLoader
from typing import Dict, Any

from glotter.models.project import NamingScheme
from glotter.settings import Settings


class ContainerInfo:
    """Configuration for a container to run for a directory"""

    def __init__(self, image: str, tag: str, cmd: str, build: str = None):
        """
        Initialize a ContainerInfo

        :param image: the image to run
        :param tag: the tag of the image to run
        :param cmd: the command to run the source inside the container
        :param build: an optional command to run to build the source before running the command
        """
        self._image = image
        self._cmd = cmd
        self._tag = tag
        self._build = build

    @property
    def image(self) -> str:
        """Returns the image to run"""
        return self._image

    @property
    def cmd(self) -> str:
        """Returns the command to run the source inside the container"""
        return self._cmd

    @property
    def tag(self) -> str:
        """Returns the tag of the image to run"""
        return self._tag

    @property
    def build(self) -> str:
        """Returns the command to build the source before running it inside the container"""
        return self._build

    @classmethod
    def from_dict(cls, dictionary: Dict[str, str]) -> ContainerInfo:
        """
        Create a ContainerInfo from a dictionary

        :param dictionary: the dictionary representing ContainerInfo
        :return: a new ContainerInfo
        """
        image = dictionary['image']
        tag = dictionary['tag']
        cmd = dictionary['cmd']
        build = dictionary['build'] if 'build' in dictionary else None
        return ContainerInfo(
            image=image,
            tag=tag,
            cmd=cmd,
            build=build
        )

    def __eq__(self, other: ContainerInfo) -> bool:
        return self.image == other.image and \
               self.cmd == other.cmd and \
               self.tag == other.tag and \
               self.build == other.build


class FolderInfo:
    """Metadata about sources in a directory"""

    def __init__(self, extension: str, naming: str):
        """
        Initialize a FolderInfo

        :param extension: the file extension that is considered as source
        :param naming: the naming scheme for files in the directory
        """
        self._extension = extension
        try:
            self._naming = NamingScheme[naming]
        except KeyError:
            raise KeyError(f'Unknown naming scheme: "{naming}"')

    @property
    def extension(self) -> str:
        """Returns the extension for sources in the directory"""
        return self._extension

    @property
    def naming(self) -> NamingScheme:
        """Returns the naming scheme for the directory"""
        return self._naming

    def get_project_mappings(self, include_extension: bool = False) -> Dict[str, str]:
        """
        Uses the naming scheme to generate the expected source names in the directory
        and create a mapping from ProjectType to source name

        :param include_extension: whether to include the extension in the source name
        :return: a dict where the key is a ProjectType and the value is the source name
        """
        extension = self.extension if include_extension else ''
        return {
            project_type: f'{project.get_project_name_by_scheme(self.naming)}{extension}'
            for project_type, project in Settings().projects.items()
        }

    def __eq__(self, other: FolderInfo) -> bool:
        return self.extension == other.extension and \
               self.naming == other.naming

    @classmethod
    def from_dict(cls, dictionary: Dict[str, str]) -> FolderInfo:
        """
        Create a FolderInfo from a dictionary

        :param dictionary: the dictionary representing FolderInfo
        :return: a new FolderInfo
        """
        return FolderInfo(dictionary['extension'], dictionary['naming'])


class TestInfo:
    """an object representation of a testinfo file"""

    def __init__(self, container_info: ContainerInfo, folder_info: FolderInfo):
        """
        Initialize a TestInfo object

        :param container_info: ContainerInfo object
        :param folder_info: FolderInfo object
        """
        self._container_info = container_info
        self._folder_info = folder_info

    @property
    def container_info(self) -> ContainerInfo:
        """Return container info section"""
        return self._container_info

    @property
    def folder_info(self) -> FolderInfo:
        """Return folder info section"""
        return self._folder_info

    @classmethod
    def from_dict(cls, dictionary: Dict[str, Dict[str, str]]) -> TestInfo:
        """
        Create a TestInfo from a dictionary

        :param dictionary: the dictionary representing TestInfo
        :return: a new TestInfo
        """
        return TestInfo(
            container_info=ContainerInfo.from_dict(dictionary['container']),
            folder_info=FolderInfo.from_dict(dictionary['folder'])
        )

    @classmethod
    def from_string(cls, string: str, source: Any) -> TestInfo:
        """
        Create a TestInfo from a string. Modify the string using Jinja2 templating. Then parse it as yaml

        :param string: contents of a testinfo file
        :param source: a source object to use for jinja2 template parsing
        :return: a new TestInfo
        """
        template = Environment(loader=BaseLoader).from_string(string)
        template_string = template.render(source=source)
        info_yaml = yaml.safe_load(template_string)
        return cls.from_dict(info_yaml)

    def __eq__(self, other: TestInfo) -> bool:
        return self.container_info == other.container_info and \
               self.folder_info == other.folder_info
