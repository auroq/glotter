import os

import pytest

from glotter.settings import Settings
from glotter.project import AcronymScheme

from test.integration.fixtures import tmp_dir, glotter_yml, glotter_yml_projects


def setup_settings(tmp_dir, path, contents):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(contents)
    return Settings(tmp_dir)


def test_locate_yml_when_glotter_yml_does_not_exist(tmp_dir):
    settings = Settings(tmp_dir)
    assert settings.yml_path is None


def test_locate_yml_when_glotter_yml_does_exist(tmp_dir, glotter_yml):
    expected = os.path.join(tmp_dir, '.glotter.yml')
    settings = setup_settings(tmp_dir, expected, glotter_yml)
    assert settings.yml_path == expected


def test_locate_yml_when_glotter_yml_is_not_at_root(tmp_dir, glotter_yml):
    expected = os.path.join(tmp_dir, 'this', 'is', 'a', 'few', 'levels', 'deeper', '.glotter.yml')
    settings = setup_settings(tmp_dir, expected, glotter_yml)
    assert settings.yml_path == expected


@pytest.mark.parametrize(('scheme_str', 'expected'),
                         [
                             ('upper', AcronymScheme.upper),
                             ('lower', AcronymScheme.lower),
                             ('two_letter_limit', AcronymScheme.two_letter_limit),
                         ])
def test_parse_acronym_scheme(scheme_str, expected, tmp_dir):
    glotter_yml = f'settings:\n  acronym_scheme: "{scheme_str}"'
    path = os.path.join(tmp_dir, '.glotter.yml')
    settings = setup_settings(tmp_dir, path, glotter_yml)
    assert settings.acronym_scheme == expected


def test_parse_projects_when_no_projects(tmp_dir):
    glotter_yml = f'settings:\n  acronym_scheme: "upper"'
    path = os.path.join(tmp_dir, '.glotter.yml')
    settings = setup_settings(tmp_dir, path, glotter_yml)
    assert settings.projects == {}


def test_parse_projects(tmp_dir, glotter_yml, glotter_yml_projects):
    path = os.path.join(tmp_dir, '.glotter.yml')
    settings = setup_settings(tmp_dir, path, glotter_yml)
    assert settings.projects == glotter_yml_projects
