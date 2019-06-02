import os
import sys
import yaml

from enum import Enum
from warnings import warn

from glotter.project import Project, AcronymScheme
from glotter.containerfactory import Singleton


def projects_enum(cls):
    settings = Settings()
    if not issubclass(cls, Enum):
        raise AttributeError('projects_enum must be called on a subclass of enum.Enum')
    settings.set_projects_enum(cls)


class Settings(metaclass=Singleton):
    def __init__(self):
        self._projects_enum = None
        self._project_root = os.path.dirname(sys.modules['__main__'].__file__)
        self._parser = SettingsParser(self._project_root)

    @property
    def projects_enum(self):
        return self._projects_enum

    def set_projects_enum(self, cls):
        if self._projects_enum is not None:
            raise AttributeError('Cannot set projects_enum more than once')
        if not issubclass(cls, Enum):
            raise AttributeError('projects_enum value must be a subclass of enum.Enum')
        self._projects_enum = cls
        self._parser.parse()


class SettingsParser:
    def __init__(self, project_root):
        self._project_root = project_root
        self._yml_path = None
        self._yml = None
        self._acronym_scheme = None
        self._projects = None

    def parse(self):
        self._yml_path = self._locate_yml()
        if self._yml_path is not None:
            self._yml = self._parse_yml()
            self._acronym_scheme = self._parse_acronym_scheme()
            self._projects = self._parse_projects()

    @property
    def project_root(self):
        return self._project_root

    @property
    def yml_path(self):
        return self._yml_path

    @property
    def yml(self):
        return self._yml

    @property
    def acronym_scheme(self):
        return self._acronym_scheme

    @property
    def projects(self):
        return self._projects

    def _parse_acronym_scheme(self):
        if 'settings' not in self._yml or 'acronym_scheme' not in self._yml['settings']:
            return
        scheme = self._yml['settings']['acronym_scheme'].lower()
        return AcronymScheme[scheme]

    def _enum_from_string(self, name):
        proj_enum = Settings().projects_enum
        for i in proj_enum:
            if name == i.name.lower():
                return i
        raise KeyError(f'projects_enum does not contain name "{name}"')

    def _parse_projects(self):
        projects = {}
        if 'projects' in self._yml:
            for k, v in self._yml['projects'].items():
                try:
                    project_name = self._enum_from_string(name=k)
                    project = Project(
                        words=v.get('words'),
                        requires_parameters=v.get('requires_parameters'),
                        acronyms=v.get('acronyms'),
                        acronym_scheme=v.get('acronym_scheme') or self._acronym_scheme,
                    )
                    projects[project_name] = project
                except KeyError:
                    warn(f'.glotter.yml contains a project that is not found in the projects_enum: "{k}"')
                    pass  # Ignore project

        return projects

    def _parse_yml(self):
        with open(self._yml_path, 'r') as f:
            contents = f.read()

        return yaml.safe_load(contents)

    def _locate_yml(self):
        for root, dirs, files in os.walk(self._project_root):
            if '.glotter.yml' in files:
                path = os.path.abspath(root)
                return os.path.join(path, '.glotter.yml')

        return None
