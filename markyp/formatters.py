"""
Generic `markyp` element formatters.
"""

from typing import Any, Callable, Dict, Sequence, Union

from xml.sax.saxutils import escape as xml_escape

from markyp import ElementType, PropertyDict, PropertyValue


__all__ = ("format_property", "format_properties", "xml_format_element", "format_element_sequence")


def format_property(name: str, value: PropertyValue) -> str:
    """
    Formatter function for element properties.

    If `value` is `None`, `name` will be returned to allow the creation of flag attributes
    such as `disabled` in HTML.

    Boolean values are converted to lower-case strings.

    Arguments:
        name: The name of the property.
        value: The value to format. `None` means the property is simply a flag
               and simply `name` should be returned.

    Returns:
        The formatted string value.
    """
    if value is None:
        return name

    if isinstance(value, bool):
        value = "true" if value else "false"

    return f"{name}=\"{value}\""


def format_properties(properties: PropertyDict, *,
                      prop_formatter: Callable[[str, PropertyValue], str] = format_property) -> str:
    """
    Formats the given dictionary as a list of element properties.

    Arguments:
        properties: The properties to format.
        prop_formatter: The function to use to turn properties to strings.

    Returns:
        The formatted string value.
    """
    return " ".join((prop_formatter(name, value) for name, value in properties.items()))


def xml_format_element(element: ElementType) -> str:
    """
    Element formatter that ensures that string elements are XML-escaped.

    Arguments:
        element: The element to format.

    Returns:
        The string formatted element.
    """
    return xml_escape(element) if isinstance(element, str) else str(element)


def format_element_sequence(elements: Sequence[Union[ElementType, None]], *,
                            element_formatter: Callable[[ElementType], str] = xml_format_element,
                            inline: bool = False) -> str:
    """
    Formats the given sequence of elements.

    Arguments:
        elements: The elements to format.
        element_formatter: The function to use to format individual elements.
        inline: Whether the elements should be formatted in one line or each of them
                should be on a separate line.

    Returns:
        The given elements as a string.
    """
    if len(elements) == 0:
        return ""

    if inline:
        separator = " "
    else:
        separator = "\n"
        elements = ("", *elements, "")

    return separator.join((element_formatter(element) for element in elements if element is not None))
