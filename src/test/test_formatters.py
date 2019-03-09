from markyp.elements import Element
from markyp.formatters import format_property,\
                              format_properties,\
                              xml_format_element,\
                              format_element_sequence

class TE(Element):
    __slots__ = ()

def test_format_property():
    for value in ("", " ", "foo", "foo, bar"):
        assert format_property(value) == f"\"{value}\""

    for value in range(0, 99, 7):
        assert format_property(value) == f"\"{value}\""
        assert format_property(value + 0.123) == f"\"{value + 0.123}\""

    assert format_property(True) == "\"true\""
    assert format_property(False) == "\"false\""

def test_format_properties():
    keys = ("foo", "bar", "int", "float", "true", "false")
    values = ("foo", "bar", 19990526, 2008.0521, True, False)
    formatted = "foo=\"foo\" bar=\"bar\" int=\"19990526\" float=\"2008.0521\" true=\"true\" false=\"false\""
    str_formatted = "foo=foo bar=bar int=19990526 float=2008.0521 true=True false=False"
    test = dict(zip(keys, values))

    assert format_properties(test) == formatted
    assert format_properties(test, value_formatter=format_property) == formatted
    assert format_properties(test, value_formatter=str) == str_formatted

def test_xml_format_element():
    assert xml_format_element("<&>\"'¢£¥€©®") == "&lt;&amp;&gt;\"'¢£¥€©®"
    assert xml_format_element(TE("<&>", arg="arg")) == "<TE arg=\"arg\">\n&lt;&amp;&gt;\n</TE>"

def test_format_element_sequence():
    elements = (
        TE(
            "foo-1",
            TE(
                "foo-inner",
                TE("foo-inner-inner")
            ),
            "foo-2"
        ),
        "bar",
        TE(baz="baz")
    )

    assert format_element_sequence(elements, inline=True) ==\
        "<TE >\nfoo-1\n<TE >\nfoo-inner\n<TE >\nfoo-inner-inner\n</TE>\n</TE>\nfoo-2\n</TE> bar <TE baz=\"baz\"></TE>"
    assert format_element_sequence(elements, inline=False) ==\
        "\n<TE >\nfoo-1\n<TE >\nfoo-inner\n<TE >\nfoo-inner-inner\n</TE>\n</TE>\nfoo-2\n</TE>\nbar\n<TE baz=\"baz\"></TE>\n"
    assert format_element_sequence(elements) ==\
        "\n<TE >\nfoo-1\n<TE >\nfoo-inner\n<TE >\nfoo-inner-inner\n</TE>\n</TE>\nfoo-2\n</TE>\nbar\n<TE baz=\"baz\"></TE>\n"
