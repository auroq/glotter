import os
import pytest

from glotter.settings import SettingsParser
from glotter.project import AcronymScheme

from test.integration.fixtures import tmp_dir, glotter_yml, glotter_yml_projects, patch_projects_enum


def setup_settings_parser(tmp_dir, path, contents):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(contents)
    return SettingsParser(tmp_dir)


def test_locate_yml_when_glotter_yml_does_not_exist(tmp_dir):
    settings_parser = SettingsParser(tmp_dir)
    settings_parser.parse_settings_section()
    assert settings_parser.yml_path is None


def test_locate_yml_when_glotter_yml_does_exist(tmp_dir, glotter_yml, patch_projects_enum):
    expected = os.path.join(tmp_dir, '.glotter.yml')
    settings_parser = setup_settings_parser(tmp_dir, expected, glotter_yml)
    settings_parser.parse_settings_section()
    assert settings_parser.yml_path == expected


def test_locate_yml_when_glotter_yml_is_not_at_root(tmp_dir, glotter_yml, patch_projects_enum):
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


def test_parses_source_root_when_path_absolute(tmp_dir):
    expected = os.path.abspath(os.path.join(tmp_dir, 'subdir'))
    os.makedirs(expected)
    glotter_yml = f'settings:\n  source_root: "{expected}"'
    path = os.path.join(tmp_dir, '.glotter.yml')
    settings_parser = setup_settings_parser(tmp_dir, path, glotter_yml)
    settings_parser.parse_settings_section()
    assert settings_parser.source_root == expected


def test_parses_source_root_when_path_relative(tmp_dir):
    expected = os.path.abspath(os.path.join(tmp_dir, 'src'))
    os.makedirs(expected)
    glotter_yml = f'settings:\n  source_root: "../src"'
    path = os.path.join(tmp_dir, 'subdir', '.glotter.yml')
    settings_parser = setup_settings_parser(tmp_dir, path, glotter_yml)
    settings_parser.parse_settings_section()
    assert settings_parser.source_root == expected


def test_parse_projects_when_no_projects_enum(tmp_dir, glotter_yml):
    path = os.path.join(tmp_dir, '.glotter.yml')
    settings_parser = setup_settings_parser(tmp_dir, path, glotter_yml)
    settings_parser.parse_settings_section()
    assert settings_parser.projects is None


def test_parse_projects_when_no_projects(tmp_dir, patch_projects_enum):
    glotter_yml = f'settings:\n  acronym_scheme: "upper"'
    path = os.path.join(tmp_dir, '.glotter.yml')
    settings_parser = setup_settings_parser(tmp_dir, path, glotter_yml)
    settings_parser.parse_projects_section()
    assert settings_parser.projects == {}


def test_parse_projects_when_no_projects_or_projects_enum(tmp_dir):
    glotter_yml = f'settings:\n  acronym_scheme: "upper"'
    path = os.path.join(tmp_dir, '.glotter.yml')
    settings_parser = setup_settings_parser(tmp_dir, path, glotter_yml)
    settings_parser.parse_projects_section()
    assert settings_parser.projects is None


def test_parse_projects(tmp_dir, glotter_yml, glotter_yml_projects, patch_projects_enum):
    path = os.path.join(tmp_dir, '.glotter.yml')
    settings_parser = setup_settings_parser(tmp_dir, path, glotter_yml)
    settings_parser.parse_projects_section()
    assert settings_parser.projects == glotter_yml_projects


def test_parse_projects_when_yml_contains_projects_not_in_enum(tmp_dir, glotter_yml, glotter_yml_projects,
                                                               patch_projects_enum, monkeypatch):
    path = os.path.join(tmp_dir, '.glotter.yml')
    glotter_yml += """
  nonexistantproject:
    words:
      - "nonexistant"
      - "project"
    requires_parameters: false
"""
    settings_parser = setup_settings_parser(tmp_dir, path, glotter_yml)
    settings_parser.parse_projects_section()
    assert settings_parser.projects == glotter_yml_projects
