from enum import Enum, auto


class NamingScheme(Enum):
    hyphen = auto()
    underscore = auto()
    camel = auto()
    pascal = auto()
    lower = auto()


class AcronymScheme(Enum):
    lower = auto()
    upper = auto()
    two_letter_limit = auto()


class Project:
    def __init__(self, words, requires_parameters=False, acronyms=None, acronym_scheme=None):
        self._words = words
        self._requires_parameters = requires_parameters
        self._acronyms = [acronym.upper() for acronym in acronyms] if acronyms else []
        self._acronym_scheme = acronym_scheme or AcronymScheme.upper

    def get_project_name_by_scheme(self, naming):
        """
        gets a project name for a specific naming scheme

        :param naming: the naming scheme
        :return: the project type formatted by the directory's naming scheme
        """
        try:
            return {
                NamingScheme.hyphen: self._as_hyphen(),
                NamingScheme.underscore: self._as_underscore(),
                NamingScheme.camel: self._as_camel(),
                NamingScheme.pascal: self._as_pascal(),
                NamingScheme.lower: self._as_lower(),
            }[naming]
        except KeyError as e:
            raise KeyError(f"Unknown naming scheme '{naming}'", e)

    def _as_hyphen(self):
        return '-'.join(map(self._try_as_acronym, self._words))

    def _as_underscore(self):
        return '_'.join(map(self._try_as_acronym, self._words))

    def _as_camel(self):
        return self._words[0].lower() + ''.join([self._try_as_acronym(word.title()) for word in self._words[1:]])

    def _as_pascal(self):
        return ''.join([self._try_as_acronym(word.title()) for word in self._words])

    def _as_lower(self):
        return ''.join([word.lower() for word in self._words])

    def _is_acronym(self, word):
        return word.upper() in self._acronyms

    def _try_as_acronym(self, word):
        if self._is_acronym(word):
            if self._acronym_scheme == AcronymScheme.upper:
                return word.upper()
            elif self._acronym_scheme == AcronymScheme.lower:
                return word.lower()
            elif self._acronym_scheme == AcronymScheme.two_letter_limit:
                if len(word) <= 2:
                    return word.upper()
        return word

    def __eq__(self, other):
        return self._words == other._words and \
               self._requires_parameters == other._requires_parameters and \
               self._acronyms == other._acronyms and \
               self._acronym_scheme == other._acronym_scheme


class ProjectType(Enum):
    Baklava = auto()
    BubbleSort = auto()
    ConvexHull = auto()
    EvenOdd = auto()
    Factorial = auto()
    Fibonacci = auto()
    FileIO = auto()
    FizzBuzz = auto()
    HelloWorld = auto()
    InsertionSort = auto()
    JobSequencing = auto()
    LCS = auto()
    MergeSort = auto()
    MST = auto()
    Prime = auto()
    QuickSort = auto()
    Quine = auto()
    ROT13 = auto()
    ReverseString = auto()
    RomanNumeral = auto()
    SelectionSort = auto()


sorting_types = [
    ProjectType.BubbleSort,
    ProjectType.InsertionSort,
    ProjectType.MergeSort,
    ProjectType.QuickSort,
    ProjectType.SelectionSort
]


def requires_params(project):
    project_mapping = {
        ProjectType.Baklava: False,
        ProjectType.BubbleSort: True,
        ProjectType.ConvexHull: True,
        ProjectType.EvenOdd: True,
        ProjectType.Factorial: True,
        ProjectType.Fibonacci: True,
        ProjectType.FileIO: False,
        ProjectType.FizzBuzz: False,
        ProjectType.HelloWorld: False,
        ProjectType.InsertionSort: True,
        ProjectType.JobSequencing: True,
        ProjectType.LCS: True,
        ProjectType.MergeSort: True,
        ProjectType.MST: True,
        ProjectType.Prime: True,
        ProjectType.QuickSort: True,
        ProjectType.Quine: False,
        ProjectType.ROT13: True,
        ProjectType.ReverseString: True,
        ProjectType.RomanNumeral: True,
        ProjectType.SelectionSort: True,
    }
    return project_mapping[project]


_project_words = {
    ProjectType.Baklava: ['baklava'],
    ProjectType.BubbleSort: ['bubble', 'sort'],
    ProjectType.ConvexHull: ['convex', 'hull'],
    ProjectType.EvenOdd: ['even', 'odd'],
    ProjectType.Factorial: ['factorial'],
    ProjectType.Fibonacci: ['fibonacci'],
    ProjectType.FileIO: ['file', 'io'],
    ProjectType.FizzBuzz: ['fizz', 'buzz'],
    ProjectType.HelloWorld: ['hello', 'world'],
    ProjectType.InsertionSort: ['insertion', 'sort'],
    ProjectType.JobSequencing: ['job', 'sequencing'],
    ProjectType.LCS: ['lcs'],
    ProjectType.MergeSort: ['merge', 'sort'],
    ProjectType.MST: ['mst'],
    ProjectType.Prime: ['prime', 'number'],
    ProjectType.QuickSort: ['quick', 'sort'],
    ProjectType.Quine: ['quine'],
    ProjectType.ROT13: ['rot', '13'],
    ProjectType.ReverseString: ['reverse', 'string'],
    ProjectType.RomanNumeral: ['roman', 'numeral'],
    ProjectType.SelectionSort: ['selection', 'sort'],
}

_project_acronyms = ['lcs', 'mst', 'io']
