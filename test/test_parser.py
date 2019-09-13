import pytest

from markyp import ElementType, PropertyDict
from markyp.elements import (
    ChildrenOnlyElement,
    Element,
    EmptyElement,
    SelfClosedElement,
    StringElement,
)
from markyp.parser import AnyElement, Converter, Parser, ParserRule


def test_converter():
    element = get_elements()
    markup = element.markup
    converted_element = get_converted_elements()
    converted_markup = converted_element.markup

    for i, parser in enumerate(get_parsers(converter)):
        parsed = parser.fromstring(markup)
        assert_elements_equal(parsed, converted_element)
        assert parsed.markup == converted_markup


def test_factory_error():
    class Foo:
        pass

    with pytest.raises(ValueError):
        Parser(Foo)

    with pytest.raises(ValueError):
        Parser((Element, "tag"))

    with pytest.raises(ValueError):
        Parser(("tag", Element, "extra-item"))


def test_parse_from_file():
    element = get_elements()
    markup = element.markup

    for i, parser in enumerate(get_parsers()):
        parsed = parser.parse("data/test/test_parser_data.xml")
        assert_elements_equal(parsed, element)
        assert parsed.markup == markup


def test_parser():
    element = get_elements()
    markup = element.markup

    for i, parser in enumerate(get_parsers()):
        parsed = parser.fromstring(markup)
        assert_elements_equal(parsed, element)
        assert parsed.markup == markup


def get_elements():
    return ChildrenOnlyElement(
        Element("Children", attr1="1"),
        EmptyElement(attr1="11", attr2="22"),
        SelfClosedElement(attr1="111", attr2="222"),
        StringElement("String children"),
        AnyElement("AnyElement content", element_tag="Any", attr="any-element"),
    )


def get_converted_elements():
    return ChildrenOnlyElement(
        Element("Children", attr1="1", converter="applied"),
        EmptyElement(attr1="11", attr2="22", converter="applied"),
        SelfClosedElement(attr1="111", attr2="222", converter="applied"),
        StringElement("String children", converter="applied"),
        AnyElement(
            "AnyElement content",
            element_tag="Any",
            attr="any-element",
            converter="applied",
        ),
    )


def assert_elements_equal(foo: ElementType, bar: ElementType):
    assert type(foo) == type(bar)

    if isinstance(foo, str):
        assert foo.strip() == bar.strip()  # type: ignore
        return

    if "properties" in foo.__slots__:
        assert foo.properties == bar.properties  # type: ignore

    if "children" in foo.__slots__:
        assert len(foo.children) == len(bar.children)  # type: ignore
        for i in range(len(foo.children)):  # type: ignore
            assert_elements_equal(foo.children[i], bar.children[i])  # type: ignore


def get_parsers(converter=None):
    parser_1 = Parser(
        ChildrenOnlyElement, Element, EmptyElement, SelfClosedElement, StringElement
    )
    parser_2 = Parser()
    parser_2.add_rules(
        [ChildrenOnlyElement, Element, EmptyElement, SelfClosedElement, StringElement]
    )
    parser_3 = Parser(("Element", ErrorElement), ("EmptyElement", ErrorElement))
    parser_3.set_rules(
        [ChildrenOnlyElement, Element, EmptyElement, SelfClosedElement, StringElement]
    )
    parser_4 = Parser(
        ("ChildrenOnlyElement", ChildrenOnlyElement),
        ("Element", Element),
        ("EmptyElement", EmptyElement),
        ("SelfClosedElement", SelfClosedElement),
        ("StringElement", StringElement),
    )
    parser_5 = Parser(
        ParserRule("ChildrenOnlyElement", ChildrenOnlyElement),
        ParserRule("Element", Element),
        ParserRule("EmptyElement", EmptyElement),
        ParserRule("SelfClosedElement", SelfClosedElement),
        ParserRule("StringElement", StringElement),
    )

    parsers = (parser_1, parser_2, parser_3, parser_4, parser_5)
    for p in parsers:
        p.converter(converter)

    return parsers


class ErrorElement(Element):
    __slots__ = ()


def converter(factory, children, properties):
    if factory == ChildrenOnlyElement:
        return factory, children, properties

    properties["converter"] = "applied"
    return factory, children, properties
