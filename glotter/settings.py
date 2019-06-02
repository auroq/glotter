import os
import sys

import yaml
from glotter.project import Project, AcronymScheme
from glotter.containerfactory import Singleton


class Settings:
    def __init__(self, project_root=None):
        self._project_root = project_root or os.path.dirname(sys.modules['__main__'].__file__)
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

    def _parse_projects(self):
        projects = {}
        if 'projects' in self._yml:
            for k, v in self._yml['projects'].items():
                projects[k] = Project(
                    words=v.get('words'),
                    requires_parameters=v.get('requires_parameters'),
                    acronyms=v.get('acronyms'),
                    acronym_scheme=v.get('acronym_scheme') or self._acronym_scheme,
                )

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
