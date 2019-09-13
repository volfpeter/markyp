"""
Markup parser.

The module is built on the `xml` module of the standard library, therefore it inherits
the standard library's security limitations.
"""

from typing import Callable, Dict, NamedTuple, Optional, Sequence, Tuple, Type, Union

import xml.etree.ElementTree as ET

from markyp import ElementType, IElement, PropertyDict, PropertyValue
from markyp.elements import Element


__all__ = ("Converter", "FactoryType", "ParserRule", "AnyElement", "Parser")


Converter = Callable[
    [Type[ElementType], Sequence[ElementType], PropertyDict],
    Tuple[Type[ElementType], Sequence[ElementType], PropertyDict],
]


class ParserRule(NamedTuple):
    """
    Tuple of tag - element factory pairs.
    """

    tag_name: str
    """
    The tag the rule applies to.
    """

    factory: Type[IElement]
    """
    The element factory to use for the corresponding tag.
    """


FactoryType = Union[Type[IElement], ParserRule]


class AnyElement(Element):
    """
    Element that can represent any tag in a markup document.
    """

    __slots__ = ("_tag",)

    def __init__(
        self,
        *args: ElementType,
        element_tag: str,
        class_: Optional[str] = None,
        **kwargs: PropertyValue,
    ) -> None:
        """
        Initialization.

        Arguments:
            element_tag: The tag name to use in markup for the document.
            class_: Additional CSS class names to set on the element.
                Overrides `kwargs["class"]` if it exists.
        """
        super().__init__(*args, class_=class_, **kwargs)
        self._tag = element_tag

    @property
    def element_name(self) -> str:
        """
        Inherited.
        """
        return self._tag


class Parser:
    """
    `markyp` element parser.

    The parser accepts the following types of rules:

    - `IElement` classes / factory types: Class that handles tags whose name matches the class' name.
    - `ParserRule` or equivalent `tuple`: Tag name - factory type pair. When the parser encounters
        an element with the given tag name, it will use the given factory type to process it.

    When the parser finds an element with a tag for which there is no registered rule, it will
    convert the element into an `AnyElement` instance, making sure the tag name, properties, and
    children of the element are all kept intact.
    """

    __slots__ = ("_converter", "_rules")

    def __init__(self, *rules: FactoryType):
        """
        Initialization.

        Positional arguments will be passed on to the `add_rules()` method. Each argument
        must be an element factory type, a `ParserRule` or an equivalent `tuple`.
        """
        self._converter: Optional[Converter] = None
        """
        Function that converts a factory type - children list - properties dictionary tuple
        into another, similar tuple that will be used for element creation.
        """

        self._rules: Dict[str, Type[ElementType]] = dict()
        """
        The rules (tag name - factory type pairs) the parser uses.
        """

        self.add_rules(rules)

    def add_rules(self, rules: Sequence[FactoryType]) -> None:
        """
        Adds the given list of rules to the parser.

        Arguments:
            rules: Element factory types or parser rules (`ParserRule` or equivalent tuple
                   instances) to add to the parser.
        """
        self._rules.update(dict(self._get_rule_entry(item) for item in rules))

    def clear_rules(self) -> None:
        """
        Clears all the rules from the parser.
        """
        self._rules.clear()

    def set_rules(self, rules: Sequence[FactoryType]) -> None:
        """
        Replaces the current rules with the provided new ones.

        Arguments:
            rules: Element factory types or parser rules (`ParserRule` or equivalent tuple
                   instances) the parser should use.
        """
        self.clear_rules()
        self.add_rules(rules)

    def converter(self, func: Optional[Converter]) -> Optional[Converter]:
        """
        Sets the factory-children-property converter of the parser to the given value.

        The method can be used as a decorator.

        Arguments:
            func: Function that takes a factory type - children sequence - properties dictionary
                  and converts it to a another, similar tuple (replacing or changing any of the
                  received values). The only requirement regarding the returned tuple is that
                  it must be possible to execute the `factory(*children, **properties)` call
                  with them.
        """
        self._converter = func
        return func

    def convert(self, node: ET.Element) -> ElementType:
        """
        Recursively converts the given element into a `markyp` element hierarchy.

        Arguments:
            node: The `etree` element to convert.

        Returns:
            The created `markyp` element hierachy.
        """
        tag = node.tag
        factory = self._rules.get(tag, AnyElement)
        children: Sequence[ElementType] = self._get_children(node)
        props = self._get_properties(node)

        if factory == AnyElement:
            props["element_tag"] = tag

        if self._converter is not None:
            factory, children, props = self._converter(factory, children, props)

        return factory(*children, **props)  # type: ignore

    def fromstring(self, data: str) -> ElementType:
        """
        Parses the given XML string.

        Arguments:
            data: The string to parse.

        Returns:
            The parsed element hierarchy.
        """
        tree = ET.fromstring(data)
        return self.convert(tree)

    def parse(self, path: str) -> ElementType:
        """
        Parses the file at the given path.

        Arguments:
            path: The path of the file to parse.

        Returns:
            The parsed element hierarchy.
        """
        tree = ET.parse(path).getroot()
        return self.convert(tree)

    def _get_children(self, node: ET.Element) -> Sequence[ElementType]:
        """
        Returns the children elements of the given `etree` element as `markyp` elements.

        Arguments:
            node: The node whose children are required.
        """
        return (
            [self.convert(item) for item in node]
            if self._is_empty_string(node.text)
            else [node.text.strip()]
            if node.text
            else []
        )

    def _get_properties(self, node: ET.Element) -> PropertyDict:
        """
        Returns the properties of the given `etree` element.

        Argument:
            node: The node whose children are required.
        """
        return {
            key: value.replace('"', "&quot;") if isinstance(value, str) else value
            for key, value in node.items()
        }

    def _get_rule_entry(self, rule: FactoryType) -> Tuple[str, Type[IElement]]:
        """
        Returns a rule entry tuple for the given rule.

        Arguments:
            rule: The rule to create the rule entry tuple from.

        Returns:
            Rule entry tuple for the given rule.

        Raises:
            ValueError: When the given rule is invalid or can not be recognized.
        """
        if isinstance(rule, ParserRule):
            return rule.tag_name, rule.factory

        if (
            isinstance(rule, tuple)
            and len(rule) == 2
            and isinstance(rule[0], str)
            and issubclass(rule[1], IElement)
        ):
            return rule

        try:
            if issubclass(rule, IElement):
                return rule.__name__, rule
        except TypeError:
            pass

        raise ValueError(f"Invalid factory rule: {rule}")

    def _is_empty_string(self, value: Optional[str]) -> bool:
        """
        Returns whether the given value is an empty string.

        Arguments:
            value: The value to check.
        """
        return value is None or value.strip() == ""

