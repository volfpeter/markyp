"""
Element handling utilities.
"""

from typing import Callable, Iterator, List, Union

from markyp import ElementType


__all__ = ("join_elements", "join_generator")


Separator = Union[ElementType, Callable[[], ElementType]]


def join_elements(items: List[ElementType], separator: Separator) -> List[ElementType]:
    """
    Returns a list that contains every element from `items` separated by the given `separator`.

    Arguments:
        items: The elements to join.
        separator: Either an element or a callable the takes no arguments and returns element.
    """
    return list(join_generator(items, separator))


def join_generator(
    items: List[ElementType], separator: Separator
) -> Iterator[ElementType]:
    """
    Generator that yields every element from `items` separated by the given `separator`.

    Arguments:
        items: The elements to join.
        separator: Either an element or a callable the takes no arguments and returns element.
    """
    sep: Callable[[], ElementType]
    if isinstance(separator, Callable):  # type: ignore
        sep = lambda: separator()  # type: ignore
    else:
        sep = lambda: separator  # type: ignore

    item_count = len(items)
    for i, item in enumerate(items):
        yield item
        if i < item_count - 1:
            yield sep()
