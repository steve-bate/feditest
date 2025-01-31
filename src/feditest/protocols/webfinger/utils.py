"""
WebFinger testing utils
"""

from typing import Any, Type

from multidict import MultiDict
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description

from feditest.protocols.webfinger.traffic import ClaimedJrd, WebFingerQueryResponse

class RecursiveEqualToMatcher(BaseMatcher):
    """
    Custom matcher: recursively match two objects
    """
    def __init__(self, other: Any):
        self._other = other


    def _matches(self, here: Any) -> bool:
        return self._equals(here, self._other)


    def _equals(self, a: Any, b: Any):
        if a is None:
            return b is None
        if b is None:
            return False
        if type(a) is not type(b):
            return False
        if isinstance(a, (int, float, str, bool)):
            return a == b
        if isinstance(a, (list, tuple, set)):
            if len(a) != len(b):
                return False
            return all(self._equals(aa, bb) for aa, bb in zip(a, b))
        if isinstance(a, dict):
            if len(a) != len(b):
                return False
            for key in a:
                if key not in b:
                    return False
                if not self._equals(a[key], b[key]):
                    return False
            return True
        if hasattr(a, '__dict__') and hasattr(b, '__dict__'):
            return self._equals(a.__dict__, b.__dict__)
        return False # not sure what else it can be


    def describe_to(self, description: Description) -> None:
        description.append_text(f'Objects must be of the same type and recursive structure: { self._other }')


class LinkSubsetOrEqualToMatcher(BaseMatcher):
    """
    Custom matcher: decide whether this JRD is the same as the provided JRD,
    or is the same with only a subset of the link elements.
    See https://pyhamcrest.readthedocs.io/en/latest/custom_matchers.html
    """
    def __init__(self, jrd_with_superset: ClaimedJrd, rels: list[str] | None = None):
        """
        jrd_with_superset: the JRD to compare against
        rels: the rels the subset is not supposed to have stripped
        """
        self._jrd_with_superset = jrd_with_superset
        self._rels = rels or [] # that makes the code below simpler


    def _matches(self, jrd_with_subset: ClaimedJrd) -> bool:
        if self._jrd_with_superset is None:
            return False
        if jrd_with_subset is None:
            return False
        return jrd_with_subset.is_valid_link_subset(self._jrd_with_superset, self._rels)


    def describe_to(self, description: Description) -> None:
        description.append_text('Links must be the same or a subset.')
        description.append_text(f'JRD: { self._jrd_with_superset }')
        if self._rels:
            description.append_text(f'rels: { ", ".join(self._rels) }')


class MultiDictHasKeyMatcher(BaseMatcher):
    """
    Custom matcher: decide whether a MultiDict has an entry with this name.
    Does not check whether there is a value or multiple values.
    """
    def __init__(self, key: str):
        self._key = key


    def _matches(self, multi_dict: MultiDict) -> bool:
        return self._key in multi_dict


    def describe_to(self, description: Description) -> None:
        description.append_text(f'MultiDict has key: { self._key }')


class NoneExceptMatcher(BaseMatcher):
    """
    Custom matcher: decode whether an Exception (which may be an ExceptionGroup) contains
    any Exception other than the provided allowed exceptions.
    """
    def __init__(self, allowed_excs: list[Type[Exception]]):
        self._allowed_excs = allowed_excs


    def _matches(self, candidate: Exception | None ) -> bool:
        if candidate is None:
            return True
        if isinstance(candidate, ExceptionGroup):
            for cand in candidate.exceptions:
                found = False
                for allowed in self._allowed_excs:
                    if isinstance(cand, allowed):
                        found = True
                if not found:
                    return False
            return True

        for allowed in self._allowed_excs:
            if isinstance(candidate, allowed):
                return True
        return False


    def describe_to(self, description: Description) -> None:
        description.append_text(f'No exception other than: { ",".join( [ x.__name__ for x in self._allowed_excs ] ) }')


def recursive_equal_to(arg: object) -> RecursiveEqualToMatcher :
    return RecursiveEqualToMatcher(arg)


def link_subset_or_equal_to(arg: ClaimedJrd) -> LinkSubsetOrEqualToMatcher :
    return LinkSubsetOrEqualToMatcher(arg)


def multi_dict_has_key(arg: str) -> MultiDictHasKeyMatcher :
    return MultiDictHasKeyMatcher(arg)


def none_except(*allowed_excs : Type[Exception]) -> NoneExceptMatcher :
    return NoneExceptMatcher(list(allowed_excs))


def wf_error(response: WebFingerQueryResponse) -> str:
    """
    Construct an error message
    """
    if not response.exc:
        return 'ok'

    if isinstance(response.exc, ExceptionGroup):
        # Make this more compact than the default
        msg = str(response.exc.args[0]).split('\n', maxsplit=1)[0]
        msg += f' ({ len(response.exc.exceptions) })'
        msg += f'\nAccessed URI: "{ response.http_request_response_pair.request.uri.get_uri() }".'
        for i, exc in enumerate(response.exc.exceptions):
            msg += f'\n{ i }: { exc }'

    else:
        msg = str(response.exc).split('\n', maxsplit=1)[0]
        msg += f'\nAccessed URI: "{ response.http_request_response_pair.request.uri.get_uri() }".'
        msg += '\n'.join(str(response.exc).split('\n')[1:])
    return msg
