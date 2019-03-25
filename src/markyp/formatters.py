"""
Generic `markyp` element formatters.
"""

from typing import Any, Callable, Dict, Sequence, Union

from xml.sax.saxutils import escape as xml_escape

from markyp import ElementType, PropertyDict, PropertyValue


def format_property(value: PropertyValue) -> str:
    """
    Formatter function for element properties.

    Arguments:
        value: The value to format.

    Returns:
        The formatted string value.
    """
    if isinstance(value, bool):
        value = "true" if value else "false"

    return f"\"{value}\""


def format_properties(properties: PropertyDict, *,
                      value_formatter: Callable[[PropertyValue], str] = format_property) -> str:
    """
    Formats the given dictionary as a list of element properties.

    Arguments:
        properties: The properties to format.
        value_formatter: The function to use to turn property values to strings.

    Returns:
        The formatted string value.
    """
    return " ".join((f"{key}={value_formatter(value)}" for key, value in properties.items()))


def xml_format_element(element: ElementType) -> str:
    """
    Element formatter that ensures that string elements are XML-escaped.

    Arguments:
        element: The element to format.

    Returns:
        The string formatted element.
    """
    return xml_escape(element) if isinstance(element, str) else str(element)


def format_element_sequence(elements: Sequence[ElementType], *,
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

    return separator.join((element_formatter(element) for element in elements))
