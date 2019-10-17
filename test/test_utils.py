from typing import Generator

from markyp import IElement
from markyp.utils import *


class SeparatorCls(IElement):
    def __new__(cls) -> str:
        return "separator"


def separator_fun():
    return "separator"


def test_join_elements():
    for separator in ("separator", separator_fun(), SeparatorCls):
        assert [] == join_elements([], separator)
        assert ["foo"] == join_elements(["foo"], separator)
        assert ["foo", "separator", "bar"] == join_elements(["foo", "bar"], separator)
        assert ["foo", "separator", "bar", "separator", "baz"] == join_elements(
            ["foo", "bar", "baz"], separator
        )


def test_join_generator():
    for separator in ("separator", separator_fun, SeparatorCls):
        result = join_generator([], separator)
        assert isinstance(result, Generator)
        assert [] == list(result)

        result = join_generator(["foo"], separator)
        assert isinstance(result, Generator)
        assert ["foo"] == list(result)

        result = join_generator(["foo", "bar"], separator)
        assert isinstance(result, Generator)
        assert ["foo", "separator", "bar"] == list(result)

        result = join_generator(["foo", "bar", "baz"], separator)
        assert isinstance(result, Generator)
        assert ["foo", "separator", "bar", "separator", "baz"] == list(result)
