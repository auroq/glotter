import os
import yaml

from enum import Enum
from warnings import warn

from glotter.project import Project, AcronymScheme
from glotter.containerfactory import Singleton
from glotter.projecthelpers import enum_from_string


def projects_enum(cls):
    settings = Settings()
    if not issubclass(cls, Enum):
        raise AttributeError('projects_enum must be called on a subclass of enum.Enum')
    settings.set_projects_enum(cls)
    return cls


def project_test(func, project_type):
    Settings().add_test_mapping(project_type, func)
    return func


class Settings(metaclass=Singleton):
    def __init__(self):
        self._projects_enum = None
        self._project_root = os.getcwd()
        self._parser = SettingsParser(self._project_root)
        self._source_root = self._parser.source_root or self._project_root
        self._test_mappings = {}

    @property
    def projects(self):
        return self._parser.projects

    @property
    def project_root(self):
        return self._project_root

    @property
    def source_root(self):
        return self._source_root

    @source_root.setter
    def source_root(self, value):
        self._source_root = value or self._project_root

    @property
    def test_mappings(self):
        return self._test_mappings

    @property
    def projects_enum(self):
        return self._projects_enum

    def get_test_mapping_name(self, project_type):
        return self._test_mappings[project_type].__name__

    def set_projects_enum(self, cls):
        if self._projects_enum is not None:
            raise AttributeError('Cannot set projects_enum more than once')
        if not issubclass(cls, Enum):
            raise AttributeError('projects_enum value must be a subclass of enum.Enum')
        self._projects_enum = cls
        self._parser.parse_projects_section()

    def add_test_mapping(self, project_type, func):
        if project_type not in self._test_mappings:
            self._test_mappings[project_type] = []
        self._test_mappings[project_type].append(func)

    @classmethod
    def get_project_type_by_name(cls, name):
        return enum_from_string(name, cls().projects_enum)


class SettingsParser:
    def __init__(self, project_root):
        self._project_root = project_root
        self._yml_path = None
        self._yml = None
        self._acronym_scheme = None
        self._projects = None
        self._source_root = None
        self._yml_path = self._locate_yml()
        if self._yml_path is not None:
            self._yml = self._parse_yml()
            self.parse_settings_section()
        else:
            warn(f'.glotter.yml not found in directory "{project_root}"')

    def parse_settings_section(self):
        if self._yml is not None:
            self._acronym_scheme = self._parse_acronym_scheme()
            self._source_root = self._parse_source_root()

    def parse_projects_section(self):
        if self.yml is not None:
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
    def source_root(self):
        return self._source_root

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

    def _parse_source_root(self):
        if 'settings' not in self._yml or 'source_root' not in self._yml['settings']:
            return

        path = self._yml['settings']['source_root']
        if os.path.isabs(path):
            return path

        yml_dir = os.path.dirname(self._yml_path)
        return os.path.abspath(os.path.join(yml_dir, path))

    def _parse_projects(self):
        if Settings().projects_enum is None:
            warn(f'Projects enum has not been set')
            return None

        projects = {}
        if 'projects' in self._yml:
            for k, v in self._yml['projects'].items():
                try:
                    project_name = enum_from_string(name=k, enum_cls=Settings().projects_enum)
                    project = Project(
                        words=v.get('words'),
                        requires_parameters=v.get('requires_parameters'),
                        acronyms=v.get('acronyms'),
                        acronym_scheme=v.get('acronym_scheme') or self._acronym_scheme,
                    )
                    projects[project_name] = project
                except KeyError:
                    warn(f'.glotter.yml contains a project that is not found in the projects_enum: "{k}"')

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
