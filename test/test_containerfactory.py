from test.mockdocker import Containers, Images
from test.fixtures import factory, container_info, source, docker, test_info_string


def test_get_image_returns_image(factory, container_info):
    result = factory.get_image(container_info, quiet=True)
    assert result == f'{container_info.image}:{container_info.tag}'


def test_get_image_downloads_image_when_not_found(factory, container_info):
    factory.get_image(container_info, quiet=True)
    assert f'{container_info.image}:{container_info.tag}' in factory._client.images.image_list


def test_get_image_returns_correct_tag(factory, container_info):
    Images.add_image(f'{container_info.image}:{container_info.tag}')
    Images.add_image(f'{container_info.image}:other-tag')
    result = factory.get_image(container_info, quiet=True)
    assert result == f'{container_info.image}:{container_info.tag}'


def test_get_container_uses_correct_image(factory, source, monkeypatch):
    monkeypatch.setattr('tempfile.mkdtemp', lambda *args, **kwargs: 'TEMP_DIR')
    monkeypatch.setattr('shutil.copy', lambda *args, **kwargs: '')
    result = factory.get_container(source)
    assert result.image == 'python:3.7-alpine'


def test_get_container_runs_container_with_correct_settings(factory, source, monkeypatch):
    monkeypatch.setattr('tempfile.mkdtemp', lambda *args, **kwargs: 'TEMP_DIR')
    monkeypatch.setattr('shutil.copy', lambda *args, **kwargs: '')
    result = factory.get_container(source)
    assert result.name.startswith(source.name)
    assert result['command'] == 'sleep 1h'
    assert result['working_dir'] == '/src'
    assert result['detach']


def test_get_container_builds_correct_volume_info(factory, source, monkeypatch):
    monkeypatch.setattr('shutil.copy', lambda *args, **kwargs: '')
    monkeypatch.setattr('tempfile.mkdtemp', lambda *args, **kwargs: 'TEMP_DIR')
    result = factory.get_container(source)
    assert result['volumes'] == {'TEMP_DIR': {'bind': '/src', 'mode': 'rw'}}


def test_cleanup_removes_container(source, factory, monkeypatch):
    monkeypatch.setattr('tempfile.mkdtemp', lambda *args, **kwargs: 'TEMP_DIR')
    monkeypatch.setattr('shutil.copy', lambda *args, **kwargs: '')
    monkeypatch.setattr('shutil.rmtree', lambda *args, **kwargs: '')
    container = factory.get_container(source)
    factory.cleanup(source)
    assert Containers.container_list[container.name].removed


def test_cleanup_removes_volume_dir(source, factory, monkeypatch):
    def verify_rmtree(path, ignore_errors=False, *args, **kwargs):
        assert path == 'TEMP_DIR'
        assert ignore_errors
    monkeypatch.setattr('tempfile.mkdtemp', lambda *args, **kwargs: 'TEMP_DIR')
    monkeypatch.setattr('shutil.copy', lambda *args, **kwargs: '')
    monkeypatch.setattr('shutil.rmtree', verify_rmtree)
    factory.get_container(source)
    factory.cleanup(source)
