import pytest

from enum import Enum, auto

from glotter.settings import Settings


class TestEnum(Enum):
    One = auto()
    Two = auto()
    Three = auto()


class TestEnumTwo(Enum):
    One = auto()
    Two = auto()
    Three = auto()


class TestNotEnum:
    pass


def test_set_projects_enum_cannot_set_to_non_enum():
    with pytest.raises(AttributeError):
        Settings().set_projects_enum(TestNotEnum)


def test_set_projects_enum_cannot_set_twice():
    Settings().set_projects_enum(TestEnum)
    with pytest.raises(AttributeError):
        Settings().set_projects_enum(TestEnumTwo)


def test_set_projects_enum_can_reset_to_same_class():
    Settings().set_projects_enum(TestEnum)
    assert Settings().projects_enum == TestEnum
    Settings().set_projects_enum(TestEnum)


def test_set_projects_enum():
    Settings().set_projects_enum(TestEnum)
    assert Settings().projects_enum == TestEnum
    Settings().set_projects_enum(TestEnum)
    assert Settings().projects_enum == TestEnum
