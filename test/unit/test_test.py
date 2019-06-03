import pytest

from glotter.test import _get_tests

list_of_tests = [
    'test/projects/test_even_odd.py::test_even_odd_invalid[even-odd.c-no input]',
    'test/projects/test_even_odd.py::test_even_odd_invalid[even-odd.c-empty input]',
    'test/projects/test_even_odd.py::test_even_odd_invalid[even-odd.c-invalid input: not a number]',
    'test/projects/test_even_odd.py::test_even_odd_valid[EvenOdd.cs-sample input: even]',
    'test/projects/test_even_odd.py::test_even_odd_valid[EvenOdd.cs-sample input: odd]',
    'test/projects/test_even_odd.py::test_even_odd_valid[EvenOdd.cs-sample input: negative even]',
    'test/projects/test_even_odd.py::test_even_odd_valid[EvenOdd.cs-sample input: negative odd]',
    'test/projects/test_even_odd.py::test_even_odd_invalid[EvenOdd.cs-no input]',
    'test/projects/test_factorial.py::test_factorial_valid[factorial.hs-sample input: four]',
    'test/projects/test_factorial.py::test_factorial_valid[factorial.hs-sample input: eight]',
    'test/projects/test_factorial.py::test_factorial_valid[factorial.hs-sample input: ten]',
    'test/projects/test_factorial.py::test_factorial_invalid[factorial.hs-sample input: zero]',
    'test/projects/test_factorial.py::test_factorial_invalid[factorial.hs-sample input: one]',
    'test/projects/test_factorial.py::test_factorial_invalid[factorial.hs-sample input: four]',
]


@pytest.mark.parametrize('test_function',
                         [
                             'test_even_odd_invalid',
                             'test_even_odd_valid',
                             'test_factorial_invalid',
                             'test_factorial_valid',
                         ])
def test_get_tests(test_function, monkeypatch):
    project_type = 'project_type'
    monkeypatch.setattr('glotter.settings.Settings.get_test_mapping_name', lambda *args, **kwargs: test_function)
    actual = _get_tests(project_type, list_of_tests)
    for t in list_of_tests:
        if test_function in t:
            assert t in actual


