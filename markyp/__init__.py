"""
Type declarations and the most basic building blocks of `markyp`.
"""

from typing import Any, Dict, TypeVar, Union

__author__ = "Peter Volf"
__copyright__ = "Copyright 2019, Peter Volf"
__email__ = "do.volfp@gmail.com"
__license__ = "MIT"
__url__ = "https://github.com/volfpeter/markyp"
__version__ = "0.1906.0"


__all__ = ("IElement", "ElementType", "PropertyValue", "PropertyDict", "is_element")


class IElement(object):
    """
    Abstract base class for markup elements.
    """

    __slots__ = ()

    def __str__(self) -> str:
        """
        Returns the string representation of the element including all its children.
        """
        raise NotImplementedError("IElement is abstract, please override __str__() in the child class.")

    @property
    def markup(self) -> str:
        """
        The string representation of the element including all its children.

        This property is just a proxy for `__str__()`.
        """
        return str(self)


ElementType = Union[IElement, str]
"""Type denoting `IElement` or string objects."""


PropertyValue = Union[str, int, float, bool, None]
"""Type to use for type hinting element properties."""


PropertyDict = Dict[str, PropertyValue]
"""Type representing property name - property value mapping."""


def is_element(item: Any) -> bool:
    """
    Returns whether the received item is an `ElementType`.

    Arguments:
        item: The item to check.
    """
    return isinstance(item, (IElement, str))
