import pytest

from glotter import settings


@pytest.fixture
def glotter_yml():
    return """
projects:
  baklava:
    words:
      - "baklava"
    requires_parameters: false
  fileio:
    words:
      - "file"
      - "io"
    requires_parameters: false
    acronyms:
      - "io"
  fibonacci:
    words:
      - "fibonacci"
    requires_parameters: true
"""


@pytest.fixture
def glotter_yml_dict():
    return {
        "projects": {
            "baklava": {
                "words": [
                    "baklava"
                ],
                "requires_parameters": False
            },
            "fileio": {
                "words": [
                    "file",
                    "io"
                ],
                "requires_parameters": False,
                "acronyms": [
                    "io"
                ]
            },
            "fibonacci": {
                "words": [
                    "fibonacci"
                ],
                "requires_parameters": True
            }
        }
    }


def test_parse_yml_parses(glotter_yml, glotter_yml_dict):
    actual = settings.parse_yml(glotter_yml)['projects']
    for project in glotter_yml_dict['projects'].keys():
        assert project in actual
