import os
import pytest

from glotter.settings import SettingsParser
from glotter.models.project import AcronymScheme

from test.integration.fixtures import glotter_yml, glotter_yml_projects, tmp_dir


def setup_settings_parser(tmp_dir, path, contents):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(contents)
    return SettingsParser(tmp_dir)


def test_locate_yml_when_glotter_yml_does_not_exist(tmp_dir):
    settings_parser = SettingsParser(tmp_dir)
    settings_parser.parse_settings_section()
    assert settings_parser.yml_path is None


def test_locate_yml_when_glotter_yml_does_exist(tmp_dir, glotter_yml):
    expected = os.path.join(tmp_dir, '.glotter.yml')
    settings_parser = setup_settings_parser(tmp_dir, expected, glotter_yml)
    settings_parser.parse_settings_section()
    assert settings_parser.yml_path == expected


def test_locate_yml_when_glotter_yml_is_not_at_root(tmp_dir, glotter_yml):
    expected = os.path.join(tmp_dir, 'this', 'is', 'a', 'few', 'levels', 'deeper', '.glotter.yml')
    settings_parser = setup_settings_parser(tmp_dir, expected, glotter_yml)
    settings_parser.parse_settings_section()
    assert settings_parser.yml_path == expected


@pytest.mark.parametrize(('scheme_str', 'expected'),
                         [
                             ('upper', AcronymScheme.upper),
                             ('lower', AcronymScheme.lower),
                             ('two_letter_limit', AcronymScheme.two_letter_limit),
                         ])
def test_parse_acronym_scheme(scheme_str, expected, tmp_dir):
    glotter_yml = f'settings:\n  acronym_scheme: "{scheme_str}"'
    path = os.path.join(tmp_dir, '.glotter.yml')
    settings_parser = setup_settings_parser(tmp_dir, path, glotter_yml)
    settings_parser.parse_settings_section()
    assert settings_parser.acronym_scheme == expected


@pytest.mark.parametrize('root_type', ['source_root'])
def test_parses_root_when_path_absolute(root_type, tmp_dir):
    expected = os.path.abspath(os.path.join(tmp_dir, 'subdir'))
    os.makedirs(expected)
    glotter_yml = f'settings:\n  {root_type}: "{expected}"'
    path = os.path.join(tmp_dir, '.glotter.yml')
    settings_parser = setup_settings_parser(tmp_dir, path, glotter_yml)
    settings_parser.parse_settings_section()
    assert settings_parser.__getattribute__(root_type) == expected


@pytest.mark.parametrize('root_type', ['source_root'])
def test_parses_root_when_path_relative(root_type, tmp_dir):
    expected = os.path.abspath(os.path.join(tmp_dir, 'src'))
    os.makedirs(expected)
    glotter_yml = f'settings:\n  {root_type}: "../src"'
    path = os.path.join(tmp_dir, 'subdir', '.glotter.yml')
    settings_parser = setup_settings_parser(tmp_dir, path, glotter_yml)
    settings_parser.parse_settings_section()
    assert settings_parser.__getattribute__(root_type) == expected


def test_parse_projects_when_no_projects(tmp_dir):
    glotter_yml = f'settings:\n  acronym_scheme: "upper"'
    path = os.path.join(tmp_dir, '.glotter.yml')
    settings_parser = setup_settings_parser(tmp_dir, path, glotter_yml)
    settings_parser.parse_projects_section()
    assert settings_parser.projects == {}


def test_parse_projects(tmp_dir, glotter_yml, glotter_yml_projects):
    path = os.path.join(tmp_dir, '.glotter.yml')
    settings_parser = setup_settings_parser(tmp_dir, path, glotter_yml)
    settings_parser.parse_projects_section()
    assert settings_parser.projects == glotter_yml_projects
