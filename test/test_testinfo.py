import pytest

from uuid import uuid4 as uuid
from glotter.testinfo import ContainerInfo, FolderInfo, TestInfo
from glotter.project import NamingScheme


@pytest.mark.parametrize('build', [uuid().hex, None], ids=['with_build', 'without_build'])
def test_container_info_from_dict(build):
    dct = {
        'image': uuid().hex,
        'tag': uuid().hex,
        'cmd': uuid().hex,
    }
    expected = ContainerInfo(
        image=dct['image'],
        tag=dct['tag'],
        cmd=dct['cmd'],
        build=build
    )
    if build is not None:
        dct['build'] = build
    info = ContainerInfo.from_dict(dct)
    assert info == expected


def test_folder_info_from_dict():
    dct = {
        'extension': '.py',
        'naming': 'underscore'
    }
    expected = FolderInfo(
        extension=dct['extension'],
        naming=dct['naming'],
    )
    info = FolderInfo.from_dict(dct)
    assert info == expected


def test_test_info_from_dict():
    container_info_dict = {
        'image': uuid().hex,
        'tag': uuid().hex,
        'cmd': uuid().hex,
    }
    ci = ContainerInfo(**container_info_dict)
    folder_info_dict = {
        'extension': '.py',
        'naming': 'underscore'
    }
    fi = FolderInfo(**folder_info_dict)
    test_info = TestInfo.from_dict({
        'container': container_info_dict,
        'folder': folder_info_dict
    })
    expected = TestInfo(container_info=ci, file_info=fi)
    assert test_info == expected
