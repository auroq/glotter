import pytest

from glotter.settings import Settings

from test.unit.fixtures import glotter_yml_projects, mock_projects


def test_add_test_mapping_when_project_type_not_in_projects(glotter_yml_projects):
    with pytest.raises(KeyError):
        Settings().add_test_mapping('notarealprojectype', None)


def test_add_test_mapping_when_project_type_has_no_mappings(glotter_yml_projects):
    def test_func(): pass
    Settings().add_test_mapping('baklava', test_func)
    assert test_func.__name__ in Settings().get_test_mapping_name('baklava')


def test_add_test_mapping_when_project_type_already_has_mapping(glotter_yml_projects):
    def test_func(): pass
    def test_func2(): pass
    Settings().add_test_mapping('baklava', test_func)
    Settings().add_test_mapping('baklava', test_func2)
    assert test_func.__name__ in Settings().get_test_mapping_name('baklava')
    assert test_func2.__name__ in Settings().get_test_mapping_name('baklava')


def test_get_test_mapping_name_when_project_type_not_found(glotter_yml_projects):
    assert Settings().get_test_mapping_name('nonexistentproject') == []
