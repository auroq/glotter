import pytest

from glotter.settings import Settings

from test.unit.fixtures import glotter_yml_projects, mock_projects


def test_add_test_mapping_when_project_type_not_in_projects(glotter_yml_projects):
    with pytest.raises(KeyError):
        Settings().add_test_mapping('notarealprojectype', None)
