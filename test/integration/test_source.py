import os

from glotter.models import source

from test.integration.fixtures import glotter_yml_projects, mock_projects, \
     test_info_string_no_build, test_info_string_with_build, tmp_dir


def get_hello_world(language):
    return {
        'python':
            "def main():\n  print('Hello, world!')\n\nif __name__ == '__main__':\n  main()""",
        'go':
            'package main\n\nimport "fmt"\n\nfunc main() {\n\tfmt.Println("Hello, World!")\n}'
    }[language]


def create_files_from_list(files):
    for file_path, contents in files.items():
        dir = os.path.dirname(file_path)
        if not os.path.isdir(dir):
            os.makedirs(dir)
        with open(file_path, 'w') as file:
            file.write(contents)


def test_get_sources_when_no_testinfo(tmp_dir, test_info_string_no_build, test_info_string_with_build,
                                      mock_projects):

    files = {
        os.path.join(tmp_dir, 'python', 'helloworld.py'): get_hello_world('python'),
        os.path.join(tmp_dir, 'go', 'hello-world.go'): get_hello_world('go'),
    }
    create_files_from_list(files)
    sources = source.get_sources(tmp_dir)
    assert not any(v for _, v in sources.items())


def test_get_sources(tmp_dir, test_info_string_no_build, test_info_string_with_build, glotter_yml_projects,
                     monkeypatch, mock_projects):
    files = {
        os.path.join(tmp_dir, 'python', 'testinfo.yml'): test_info_string_no_build,
        os.path.join(tmp_dir, 'python', 'hello_world.py'): get_hello_world('python'),
        os.path.join(tmp_dir, 'go', 'testinfo.yml'): test_info_string_with_build,
        os.path.join(tmp_dir, 'go', 'hello-world.go'): get_hello_world('go'),
    }
    create_files_from_list(files)
    sources = source.get_sources(tmp_dir)
    assert len(sources["helloworld"]) == 2
    assert not any(source_list for project_type, source_list in sources.items()
                   if project_type != "helloworld" and len(source_list) > 0)
