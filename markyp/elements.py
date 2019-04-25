"""
Base `markyp` element implementations.
"""

from typing import List, Sequence, Optional

from markyp import ElementType, IElement, PropertyDict, PropertyValue, is_element
from markyp.formatters import format_element_sequence, format_properties, xml_format_element, xml_escape


__all__ = (
    "BaseElement", "ChildrenOnlyElement", "Element", "ElementSequence",
    "EmptyElement", "SelfClosedElement", "StandaloneElement", "StringElement"
)


class BaseElement(IElement):
    """
    Base class for elements that calculate their own properties and children elements
    only when the markup is created.

    Define `__slots__` in derived classes to enjoy the performance benefits the feature provides.
    """

    __slots__ = ()

    def __str__(self) -> str:
        name = self.element_name
        properties = self.get_element_properties()
        properties_str = format_properties(properties) if properties is not None else ""
        children = self.get_element_children()
        children_str =\
            format_element_sequence(children,  element_formatter=xml_format_element, inline=self.inline_children)\
            if children is not None else ""
        return f"<{name} {properties_str}>{children_str}</{name}>"

    @property
    def element_name(self) -> str:
        """
        The name of the element.

        The default value is `self.__class__.__name__`.
        """
        return self.__class__.__name__

    @property
    def inline_children(self) -> bool:
        """
        Whether the children of the element should be placed on the same line as the element.

        The default value is `False`.
        """
        return False

    def get_element_children(self) -> Optional[Sequence[ElementType]]:
        """
        Returns the children elements of the element if it has children.
        """
        return None

    def get_element_properties(self) -> Optional[PropertyDict]:
        """
        Returns the element properties dictionary if the element has properties.
        """
        return None


class ChildrenOnlyElement(IElement):
    """
    Base class for elements that have no properties, only children.

    Define `__slots__` in derived classes to enjoy the performance benefits the feature provides.
    """

    __slots__ = ("children",)

    def __init__(self, *args: ElementType) -> None:
        """
        Initialization.

        An arbitrary number of positional arguments are accepted that must be either `IElement`
        instances or strings. Each positional argument will become a child of the element.
        """
        self.children: Sequence[ElementType] = args
        """The child elements."""

    def __str__(self) -> str:
        name: str = self.element_name
        return f"<{name}>{format_element_sequence(self.children, element_formatter=xml_format_element, inline=self.inline_children)}</{name}>"

    @property
    def element_name(self) -> str:
        """
        The name of the element.

        The default value is `self.__class__.__name__`.
        """
        return self.__class__.__name__

    @property
    def inline_children(self) -> bool:
        """
        Whether the children of the element should be placed on the same line as the element.

        The default value is `False`.
        """
        return False


class Element(IElement):
    """
    Base class for elements that have both properties and children.

    Child elements will be placed on new lines and string children will be XML-escaped by default.

    Define `__slots__` in derived classes to enjoy the performance benefits the feature provides.
    """

    __slots__ = ("children", "properties")

    def __init__(self, *args: ElementType, class_: Optional[str] = None, **kwargs: PropertyValue) -> None:
        """
        Initialization.

        An arbitrary number of positional arguments are accepted that must be either `IElement`
        instances or strings. Each positional argument will become a child of the element.

        The `class_` keyword argument is converted into the `class` element property,
        other keyword arguments are converted to element properties as they were defined.
        """
        self.children: Sequence[ElementType] = args
        """The child elements."""

        self.properties: PropertyDict = kwargs
        """The properties to set on the element."""

        if class_ is not None:
            self.properties["class"] = class_

    def __str__(self) -> str:
        name: str = self.element_name
        return f"<{name} {format_properties(self.properties)}>{format_element_sequence(self.children, element_formatter=xml_format_element, inline=self.inline_children)}</{name}>"

    @property
    def element_name(self) -> str:
        """
        The name of the element.

        The default value is `self.__class__.__name__`.
        """
        return self.__class__.__name__

    @property
    def inline_children(self) -> bool:
        """
        Whether the children of the element should be placed on the same line as the element.

        The default value is `False`.
        """
        return False


class ElementSequence(ChildrenOnlyElement):
    """
    `ChildrenOnlyElement` without the opening and closing tags, i.e. effectively a sequence of elements.
    """

    __slots__ = ()

    def __str__(self) -> str:
        return "" if len(self.children) == 0 else "\n".join((xml_format_element(element) for element in self.children))


class EmptyElement(IElement):
    """
    Base class for elements that have no children, only properties.

    Define `__slots__` in derived classes to enjoy the performance benefits the feature provides.
    """

    __slots__ = ("properties",)

    def __init__(self, *, class_: Optional[str] = None, **kwargs: PropertyValue) -> None:
        """
        Initialization.

        The `class_` keyword argument is converted into the `class` element property,
        other keyword arguments are converted to element properties as they were defined.
        """
        self.properties: PropertyDict = kwargs
        """The properties to set on the element."""

        if class_ is not None:
            self.properties["class"] = class_

    def __str__(self) -> str:
        name: str = self.element_name
        return f"<{name} {format_properties(self.properties)}></{name}>"

    @property
    def element_name(self) -> str:
        """
        The name of the element.

        The default value is `self.__class__.__name__`.
        """
        return self.__class__.__name__


class SelfClosedElement(EmptyElement):
    """
    Self-closed version of `EmptyElement`.

    Define `__slots__` in derived classes to enjoy the performance benefits the feature provides.
    """

    __slots__ = ()

    def __str__(self) -> str:
        return f"<{self.element_name} {format_properties(self.properties)}/>"


class StandaloneElement(EmptyElement):
    """
    A stand-alone version of `EmptyElement` that has no closing tag.

    Define `__slots__` in derived classes to enjoy the performance benefits the feature provides.
    """

    __slots__ = ()

    def __str__(self) -> str:
        return f"<{self.element_name} {format_properties(self.properties)}>"


class StringElement(IElement):
    """
    Base class for elements that have a single string children and any number of properties.

    Define `__slots__` in derived classes to enjoy the performance benefits the feature provides.
    """

    __slots__ = ("properties", "value")

    def __init__(self, value: str, *, class_: Optional[str] = None, **kwargs: PropertyValue) -> None:
        """
        Initialization.

        The `class_` keyword argument is converted into the `class` element property,
        other keyword arguments are converted to element properties as they were defined.

        Arguments:
            value: The string value of the element, it will be XML-escaped automatically
                   when the element is converted to a string.
            class_: Optional keyword argument that is converted into the `class` element property.
        """
        self.value: str = value
        """The string value of the element."""

        self.properties: PropertyDict = kwargs
        """The properties to set on the element."""

        if class_ is not None:
            self.properties["class"] = class_

    def __str__(self) -> str:
        name: str = self.element_name
        value = xml_escape(self.value) if self.value is not None else ""
        return f"<{name} {format_properties(self.properties)}>{value}</{name}>"

    @property
    def element_name(self) -> str:
        """
        The name of the element.

        The default value is `self.__class__.__name__`.
        """
        return self.__class__.__name__
