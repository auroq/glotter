import shutil
import tempfile

import pytest

from glotter.project import Project


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
def glotter_yml_projects():
    return {
        "baklava": Project(
            words=["baklava"],
            requires_parameters=False,
        ),
        "fileio": Project(
            words=["file", "io"],
            requires_parameters=False,
            acronyms=["io"]
        ),
        "fibonacci": Project(
            words=["fibonacci"],
            requires_parameters=True
        )
    }


@pytest.fixture
def test_info_string_no_build():
    return """folder:
  extension: ".py"
  naming: "underscore"

container:
  image: "python"
  tag: "3.7-alpine"
  cmd: "python {{ source.name }}{{ source.extension }}"
"""


@pytest.fixture
def test_info_string_with_build():
    return """folder:
  extension: ".go"
  naming: "hyphen"

container:
  image: "golang"
  tag: "1.12-alpine"
  build: "go build -o {{ source.name }} {{ source.name}}{{ source.extension }}"
  cmd: "./{{ source.name }}"
"""


@pytest.fixture
def tmp_dir():
    dir = tempfile.mkdtemp()
    yield dir
    shutil.rmtree(dir, ignore_errors=True)
