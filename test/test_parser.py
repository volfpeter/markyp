from markyp import ElementType
from markyp.elements import (
    ChildrenOnlyElement,
    Element,
    EmptyElement,
    SelfClosedElement,
    StringElement,
)
from markyp.parser import Parser, ParserRule


def test_parser():
    element = get_root_element()
    generated = element.markup

    for i, parser in enumerate(get_parsers()):
        parsed = parser.fromstring(generated)
        assert_elements_equal(parsed, element)
        assert parsed.markup == generated


def get_root_element():
    return ChildrenOnlyElement(
        Element("Children", attr1="1"),
        EmptyElement(attr1="11", attr2="22"),
        SelfClosedElement(attr1="111", attr2="222", class_="self-closed"),
        StringElement("String children"),
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


def get_parsers():
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
    return (parser_1, parser_2, parser_3, parser_4, parser_5)


class ErrorElement(Element):
    __slots__ = ()
