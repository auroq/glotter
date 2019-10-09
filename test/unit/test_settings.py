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

