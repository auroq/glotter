from __future__ import annotations

from enum import Enum, auto
from typing import List, Optional


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
    def __init__(self, words: List[str],
                 requires_parameters: bool = False,
                 acronyms: List[str] = None,
                 acronym_scheme: Optional[AcronymScheme] = None):
        self._words = words
        self._requires_parameters = requires_parameters
        self._acronyms = [acronym.upper() for acronym in acronyms] if acronyms else []
        self._acronym_scheme = acronym_scheme or AcronymScheme.two_letter_limit

    @property
    def words(self) -> List[str]:
        return self._words

    @property
    def requires_parameters(self) -> bool:
        return self._requires_parameters

    @property
    def acronyms(self) -> List[str]:
        return self._acronyms

    @property
    def acronym_scheme(self) -> AcronymScheme:
        return self._acronym_scheme

    @property
    def display_name(self) -> str:
        return self._as_display()

    def get_project_name_by_scheme(self, naming: NamingScheme) -> str:
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

    def _as_hyphen(self) -> str:
        return '-'.join([self._try_as_acronym(word, NamingScheme.hyphen) for word in self._words])

    def _as_underscore(self) -> str:
        return '_'.join([self._try_as_acronym(word, NamingScheme.underscore) for word in self._words])

    def _as_camel(self) -> str:
        return self._words[0].lower() + ''.join([self._try_as_acronym(word.title(), NamingScheme.camel)
                                                 for word in self.words[1:]])

    def _as_pascal(self) -> str:
        return ''.join([self._try_as_acronym(word.title(), NamingScheme.pascal) for word in self._words])

    def _as_lower(self) -> str:
        return ''.join([word.lower() for word in self._words])

    def _as_display(self) -> str:
        return ' '.join([self._try_as_acronym(word.title(), NamingScheme.underscore) for word in self._words])

    def _is_acronym(self, word) -> bool:
        return word.upper() in self._acronyms

    def _try_as_acronym(self, word: str, naming_scheme: NamingScheme) -> str:
        if self._is_acronym(word):
            if self._acronym_scheme == AcronymScheme.upper:
                return word.upper()
            elif self._acronym_scheme == AcronymScheme.lower:
                return word.lower()
            elif self._acronym_scheme == AcronymScheme.two_letter_limit:
                if len(word) <= 2 and naming_scheme in [NamingScheme.camel, NamingScheme.pascal]:
                    return word.upper()
        return word

    def __eq__(self, other: Project) -> bool:
        return self._words == other.words and \
               self._requires_parameters == other.requires_parameters and \
               self._acronyms == other.acronyms and \
               self._acronym_scheme == other.acronym_scheme
