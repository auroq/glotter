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

    @property
    def words(self):
        return self._words

    @property
    def requires_parameters(self):
        return self._requires_parameters

    @property
    def acronyms(self):
        return self._acronyms

    @property
    def acronym_scheme(self):
        return self._acronym_scheme

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
