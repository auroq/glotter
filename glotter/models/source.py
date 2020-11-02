from __future__ import annotations

import os
from typing import Dict, List

import yaml
from docker.models.containers import ExecResult

from glotter.models.testinfo import TestInfo, FolderInfo
from glotter.settings import Settings
from glotter.containerfactory import ContainerFactory


class Source:
    """Metadata about a source file"""

    def __init__(self, name: str, language: str, path: str, test_info_string: str):
        """Initialize source

        :param name: filename including extension
        :param path: path to the file excluding name
        :param language: the language of the source
        :param test_info_string: a string in yaml format containing testinfo for a directory
        """
        self._name = name
        self._language = language
        self._path = path

        self._test_info = TestInfo.from_string(test_info_string, self)

    @property
    def full_path(self) -> str:
        """Returns the full path to the source including filename and extension"""
        return os.path.join(self._path, self._name)

    @property
    def path(self) -> str:
        """Returns the path to the source excluding name"""
        return self._path

    @property
    def name(self) -> str:
        """Returns the name of the source excluding the extension"""
        return os.path.splitext(self._name)[0]

    @property
    def language(self) -> str:
        """Returns the language of the source"""
        return self._language

    @property
    def extension(self) -> str:
        """Returns the extension of the source"""
        return os.path.splitext(self._name)[1]

    @property
    def test_info(self) -> TestInfo:
        """Returns parsed TestInfo object"""
        return self._test_info

    def __repr__(self) -> str:
        return f'Source(name: {self.name}, path: {self.path})'

    def build(self, params: str = '') -> None:
        """
        Execute the sources build command inside a container.
        Noop if the source has no build command.

        :param params: input passed to the build command
        """
        if self.test_info.container_info.build is not None:
            command = f'{self.test_info.container_info.build} {params}'
            result = self._container_exec(command)
            if result[0] != 0:
                raise RuntimeError(f'unable to build using cmd "{self.test_info.container_info.build} {params}":\n'
                                   f'{result[1].decode("utf-8")}')

    def run(self, params: str = None) -> str:
        """
        Run the source and return the output

        :param params: input passed to the source as it's run
        :return: the output of running the source
        """
        params = params or ''
        command = f'{self.test_info.container_info.cmd} {params}'
        result = self._container_exec(command)
        return result[1].decode('utf-8')

    def exec(self, command: str) -> str:
        """
        Run a command inside the container for a source

        :param command: command to run
        :return:  the output of the command as a string
        """
        result = self._container_exec(command)
        return result[1].decode('utf-8')

    def _container_exec(self, command: str) -> ExecResult:
        """
        Run a command inside the container for a source

        :param command: command to run
        :return:  the exit code and output of the command
        """
        container = ContainerFactory().get_container(self)
        return container.exec_run(
            cmd=command,
            detach=False,
            workdir='/src',
        )

    def cleanup(self) -> None:
        """ Cleanup all resources created for the source on the host """
        ContainerFactory().cleanup(self)


def get_sources(path: str) -> Dict[str, List[Source]]:
    """
    Walk through a directory and create Source objects

    :param path: path to the directory through which to walk
    :return: a dict where the key is the ProjectType and the value is a list of all the Source objects of that project
    """
    sources = {k: [] for k in Settings().projects}
    for root, dirs, files in os.walk(path):
        path = os.path.abspath(root)
        if "testinfo.yml" in files:
            with open(os.path.join(path, 'testinfo.yml'), 'r') as file:
                test_info_string = file.read()
            folder_info = FolderInfo.from_dict(yaml.safe_load(test_info_string)['folder'])
            folder_project_names = folder_info.get_project_mappings(include_extension=True)
            for project_type, project_name in folder_project_names.items():
                if project_name in files:
                    source = Source(project_name, os.path.basename(path), path, test_info_string)
                    sources[project_type].append(source)
    return sources
