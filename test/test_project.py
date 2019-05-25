import pytest

from glotter.project import Project, NamingScheme

project_scheme_permutation_map = [
    {
        "id": "singe_word_no_acronym",
        "words": ["word"],
        "acronyms": None,
        "schemes": {
            NamingScheme.hyphen: "word",
            NamingScheme.underscore: "word",
            NamingScheme.camel: "word",
            NamingScheme.pascal: "Word",
            NamingScheme.lower: "word",
        }},
    {
        "id": "multiple_words_no_acronym",
        "words": ["multiple", "words"],
        "acronyms": None,
        "schemes": {
            NamingScheme.hyphen: "multiple-words",
            NamingScheme.underscore: "multiple_words",
            NamingScheme.camel: "multipleWords",
            NamingScheme.pascal: "MultipleWords",
            NamingScheme.lower: "multiplewords",
        }},
    {
        "id": "single_acronym",
        "words": ["io"],
        "acronyms": ["IO"],
        "schemes": {
            NamingScheme.hyphen: "IO",
            NamingScheme.underscore: "IO",
            NamingScheme.camel: "io",
            NamingScheme.pascal: "IO",
            NamingScheme.lower: "io",
        }},
    {
        "id": "multiple_words_with_acronym_at_front",
        "words": ["io", "word"],
        "acronyms": ["IO"],
        "schemes": {
            NamingScheme.hyphen: "IO-word",
            NamingScheme.underscore: "IO_word",
            NamingScheme.camel: "ioWord",
            NamingScheme.pascal: "IOWord",
            NamingScheme.lower: "ioword",
        }},
    {
        "id": "multiple_words_with_acronym_in_middle",
        "words": ["words", "IO", "multiple"],
        "acronyms": ["IO"],
        "schemes": {
            NamingScheme.hyphen: "words-IO-multiple",
            NamingScheme.underscore: "words_IO_multiple",
            NamingScheme.camel: "wordsIOMultiple",
            NamingScheme.pascal: "WordsIOMultiple",
            NamingScheme.lower: "wordsiomultiple",
        }},
    {
        "id": "multiple_words_with_acronym_at_end",
        "words": ["multiple", "words", "IO"],
        "acronyms": ["IO"],
        "schemes": {
            NamingScheme.hyphen: "multiple-words-IO",
            NamingScheme.underscore: "multiple_words_IO",
            NamingScheme.camel: "multipleWordsIO",
            NamingScheme.pascal: "MultipleWordsIO",
            NamingScheme.lower: "multiplewordsio",
        }},
    {
        "id": "same_acronym_twice",
        "words": ["io", "word", "io"],
        "acronyms": ["io"],
        "schemes": {
            NamingScheme.hyphen: "IO-word-IO",
            NamingScheme.underscore: "IO_word_IO",
            NamingScheme.camel: "ioWordIO",
            NamingScheme.pascal: "IOWordIO",
            NamingScheme.lower: "iowordio",
        }},
    {
        "id": "multiple_acronyms",
        "words": ["io", "word", "ui"],
        "acronyms": ["ui", "io"],
        "schemes": {
            NamingScheme.hyphen: "IO-word-UI",
            NamingScheme.underscore: "IO_word_UI",
            NamingScheme.camel: "ioWordUI",
            NamingScheme.pascal: "IOWordUI",
            NamingScheme.lower: "iowordui",
        }},
    {
        "id": "multiple_acronyms_together",
        "words": ["word", "io", "ui"],
        "acronyms": ["ui", "io"],
        "schemes": {
            NamingScheme.hyphen: "word-IO-UI",
            NamingScheme.underscore: "word_IO_UI",
            NamingScheme.camel: "wordIOUI",
            NamingScheme.pascal: "WordIOUI",
            NamingScheme.lower: "wordioui",
        }
    },
]


def get_project_scheme_permutations():
    for perm in project_scheme_permutation_map:
        id = perm["id"]
        words = perm["words"]
        acronyms = perm["acronyms"]
        for scheme, expected in perm["schemes"].items():
            yield (id, words, acronyms, scheme, expected)


@pytest.mark.parametrize(("words", "acronyms", "scheme", "expected"),
                         [perm[1:] for perm in get_project_scheme_permutations()],
                         ids=[f'{perm[0]}_{perm[3]}' for perm in get_project_scheme_permutations()])
def test_get_project_name_by_scheme(words, acronyms, scheme, expected):
    project = Project(words, acronyms=acronyms)
    actual = project.get_project_name_by_scheme(scheme)
    assert actual == expected
