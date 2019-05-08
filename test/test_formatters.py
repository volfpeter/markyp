from markyp.elements import Element
from markyp.formatters import format_property,\
                              format_properties,\
                              xml_format_element,\
                              format_element_sequence

class TE(Element):
    __slots__ = ()

def test_format_property():
    for value in ("", " ", "foo", "foo, bar"):
        assert format_property("prop_name", value) == f"prop_name=\"{value}\""

    for value in range(0, 99, 7):
        assert format_property("prop_name", value) == f"prop_name=\"{value}\""
        assert format_property("prop_name", value + 0.123) == f"prop_name=\"{value + 0.123}\""

    assert format_property("prop_name", True) == "prop_name=\"true\""
    assert format_property("prop_name", False) == "prop_name=\"false\""
    assert format_property("prop_name", None) == "prop_name"

def test_format_properties():
    def str_formatter(name, value):
        return f"{name}={value}"

    keys = ("foo", "bar", "int", "float", "true", "false", "none")
    values = ("foo", "bar", 19990526, 2008.0521, True, False, None)
    formatted = "foo=\"foo\" bar=\"bar\" int=\"19990526\" float=\"2008.0521\" true=\"true\" false=\"false\" none"
    str_formatted = "foo=foo bar=bar int=19990526 float=2008.0521 true=True false=False none=None"
    test = dict(zip(keys, values))

    assert format_properties(test) == formatted
    assert format_properties(test, prop_formatter=format_property) == formatted
    assert format_properties(test, prop_formatter=str_formatter) == str_formatted

def test_xml_format_element():
    assert xml_format_element("<&>\"'¢£¥€©®") == "&lt;&amp;&gt;\"'¢£¥€©®"
    assert xml_format_element(TE("<&>", arg="arg")) == "<TE arg=\"arg\">\n&lt;&amp;&gt;\n</TE>"

def test_format_element_sequence():
    elements = (
        None,
        TE(
            "foo-1",
            TE(
                "foo-inner",
                None,
                TE("foo-inner-inner")
            ),
            None,
            "foo-2"
        ),
        "bar",
        None,
        TE(baz="baz"),
        None
    )

    assert format_element_sequence(elements, inline=True) ==\
        "<TE >\nfoo-1\n<TE >\nfoo-inner\n<TE >\nfoo-inner-inner\n</TE>\n</TE>\nfoo-2\n</TE> bar <TE baz=\"baz\"></TE>"
    assert format_element_sequence(elements, inline=False) ==\
        "\n<TE >\nfoo-1\n<TE >\nfoo-inner\n<TE >\nfoo-inner-inner\n</TE>\n</TE>\nfoo-2\n</TE>\nbar\n<TE baz=\"baz\"></TE>\n"
    assert format_element_sequence(elements) ==\
        "\n<TE >\nfoo-1\n<TE >\nfoo-inner\n<TE >\nfoo-inner-inner\n</TE>\n</TE>\nfoo-2\n</TE>\nbar\n<TE baz=\"baz\"></TE>\n"

    assert format_element_sequence(["<markup></markup>"], element_formatter=str) == "\n<markup></markup>\n"
    assert format_element_sequence(["<markup></markup>"], inline=True) == "&lt;markup&gt;&lt;/markup&gt;"
