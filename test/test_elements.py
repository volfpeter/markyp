from markyp.elements import BaseElement,\
                            ChildrenOnlyElement,\
                            Element,\
                            ElementSequence,\
                            EmptyElement,\
                            SelfClosedElement,\
                            StandaloneElement,\
                            StringElement

def test_BaseElement():
    class TE(BaseElement):
        __slots__ = ("children", "properties")

        def __init__(self):
            super().__init__()
            self.children = None
            self.properties = None

        def get_element_children(self):
            assert super().get_element_children() is None
            return self.children

        def get_element_properties(self):
            assert super().get_element_properties() is None
            return self.properties

    te = TE()
    assert str(te) == "<TE ></TE>"

    te.children = []
    te.properties = {}
    assert str(te) == "<TE ></TE>"

    te.children = ["First", "Second"]
    te.properties = {}
    assert str(te) == "<TE >\nFirst\nSecond\n</TE>"

    te.children = ["First", "Second"]
    te.properties = {"class": "test", "width": 200}
    assert str(te) == "<TE class=\"test\" width=\"200\">\nFirst\nSecond\n</TE>"

def test_ChildrenOnlyElement():
    class TE(ChildrenOnlyElement):
        __slots__ = ()

    assert ChildrenOnlyElement().markup ==\
        "<ChildrenOnlyElement></ChildrenOnlyElement>"
    assert str(ChildrenOnlyElement()) ==\
        "<ChildrenOnlyElement></ChildrenOnlyElement>"
    assert TE().markup == "<TE></TE>"
    assert str(TE()) == "<TE></TE>"


    assert ChildrenOnlyElement("foo", "bar").markup ==\
        "<ChildrenOnlyElement>\nfoo\nbar\n</ChildrenOnlyElement>"
    assert str(ChildrenOnlyElement("foo", "bar")) ==\
        "<ChildrenOnlyElement>\nfoo\nbar\n</ChildrenOnlyElement>"
    assert TE("foo", "bar").markup == "<TE>\nfoo\nbar\n</TE>"
    assert str(TE("foo", "bar")) == "<TE>\nfoo\nbar\n</TE>"

    assert ChildrenOnlyElement(ChildrenOnlyElement("foo"), "bar").markup ==\
        "<ChildrenOnlyElement>\n<ChildrenOnlyElement>\nfoo\n</ChildrenOnlyElement>\nbar\n</ChildrenOnlyElement>"
    assert str(ChildrenOnlyElement(ChildrenOnlyElement("foo"), "bar")) ==\
        "<ChildrenOnlyElement>\n<ChildrenOnlyElement>\nfoo\n</ChildrenOnlyElement>\nbar\n</ChildrenOnlyElement>"
    assert TE(TE("foo"), "bar").markup == "<TE>\n<TE>\nfoo\n</TE>\nbar\n</TE>"
    assert str(TE(TE("foo"), "bar")) == "<TE>\n<TE>\nfoo\n</TE>\nbar\n</TE>"

    assert ChildrenOnlyElement("bar", ChildrenOnlyElement("foo")).markup ==\
        "<ChildrenOnlyElement>\nbar\n<ChildrenOnlyElement>\nfoo\n</ChildrenOnlyElement>\n</ChildrenOnlyElement>"
    assert str(ChildrenOnlyElement("bar", ChildrenOnlyElement("foo"))) ==\
        "<ChildrenOnlyElement>\nbar\n<ChildrenOnlyElement>\nfoo\n</ChildrenOnlyElement>\n</ChildrenOnlyElement>"
    assert TE("bar", TE("foo")).markup == "<TE>\nbar\n<TE>\nfoo\n</TE>\n</TE>"
    assert str(TE("bar", TE("foo"))) == "<TE>\nbar\n<TE>\nfoo\n</TE>\n</TE>"

    assert ChildrenOnlyElement("bar", ChildrenOnlyElement("foo"), "baz").markup ==\
        "<ChildrenOnlyElement>\nbar\n<ChildrenOnlyElement>\nfoo\n</ChildrenOnlyElement>\nbaz\n</ChildrenOnlyElement>"
    assert str(ChildrenOnlyElement("bar", ChildrenOnlyElement("foo"), "baz")) ==\
        "<ChildrenOnlyElement>\nbar\n<ChildrenOnlyElement>\nfoo\n</ChildrenOnlyElement>\nbaz\n</ChildrenOnlyElement>"
    assert TE("bar", TE("foo"), "baz").markup == "<TE>\nbar\n<TE>\nfoo\n</TE>\nbaz\n</TE>"
    assert str(TE("bar", TE("foo"), "baz")) == "<TE>\nbar\n<TE>\nfoo\n</TE>\nbaz\n</TE>"

def test_Element():
    class TE(Element):
        __slots__ = ()

    assert Element().markup == "<Element ></Element>"
    assert str(Element()) == "<Element ></Element>"
    assert TE().markup == "<TE ></TE>"
    assert str(TE()) == "<TE ></TE>"

    assert Element("foo", Element(), "bar").markup == "<Element >\nfoo\n<Element ></Element>\nbar\n</Element>"
    assert str(Element("foo", Element(), "bar")) == "<Element >\nfoo\n<Element ></Element>\nbar\n</Element>"
    assert TE("foo", TE(), "bar").markup == "<TE >\nfoo\n<TE ></TE>\nbar\n</TE>"
    assert str(TE("foo", TE(), "bar")) == "<TE >\nfoo\n<TE ></TE>\nbar\n</TE>"

    assert Element("foo", Element(Element("baz")), "bar").markup == "<Element >\nfoo\n<Element >\n<Element >\nbaz\n</Element>\n</Element>\nbar\n</Element>"
    assert str(Element("foo", Element(Element("baz")), "bar")) == "<Element >\nfoo\n<Element >\n<Element >\nbaz\n</Element>\n</Element>\nbar\n</Element>"
    assert TE("foo", TE(TE("baz")), "bar").markup == "<TE >\nfoo\n<TE >\n<TE >\nbaz\n</TE>\n</TE>\nbar\n</TE>"
    assert str(TE("foo", TE(TE("baz")), "bar")) == "<TE >\nfoo\n<TE >\n<TE >\nbaz\n</TE>\n</TE>\nbar\n</TE>"

    assert Element(class_="class test", value=123).markup == "<Element value=\"123\" class=\"class test\"></Element>"
    assert str(Element(class_="class test", value=123)) == "<Element value=\"123\" class=\"class test\"></Element>"
    assert TE(class_="class test", value=123).markup == "<TE value=\"123\" class=\"class test\"></TE>"
    assert str(TE(class_="class test", value=123)) == "<TE value=\"123\" class=\"class test\"></TE>"

    assert Element("foo", Element(Element("baz")), "bar", class_="class test", value=4.2).markup ==\
        "<Element value=\"4.2\" class=\"class test\">\nfoo\n<Element >\n<Element >\nbaz\n</Element>\n</Element>\nbar\n</Element>"
    assert str(Element("foo", Element(Element("baz")), "bar", class_="class test", value=4.2)) ==\
        "<Element value=\"4.2\" class=\"class test\">\nfoo\n<Element >\n<Element >\nbaz\n</Element>\n</Element>\nbar\n</Element>"
    assert TE("foo", TE(TE("baz")), "bar", class_="class test", value=4.2).markup ==\
        "<TE value=\"4.2\" class=\"class test\">\nfoo\n<TE >\n<TE >\nbaz\n</TE>\n</TE>\nbar\n</TE>"
    assert str(TE("foo", TE(TE("baz")), "bar", class_="class test", value=4.2)) ==\
        "<TE value=\"4.2\" class=\"class test\">\nfoo\n<TE >\n<TE >\nbaz\n</TE>\n</TE>\nbar\n</TE>"

def test_ElementSequence():
    assert ElementSequence().markup == ""
    assert str(ElementSequence()) == ""

    es = ElementSequence(
        Element(),
        "string element",
        SelfClosedElement()
    )
    assert es.markup == "<Element ></Element>\nstring element\n<SelfClosedElement />"
    assert str(es) == "<Element ></Element>\nstring element\n<SelfClosedElement />"

def test_EmptyElement():
    class TE(EmptyElement):
        __slots__ = ()

    assert EmptyElement().markup == "<EmptyElement ></EmptyElement>"
    assert str(EmptyElement()) == "<EmptyElement ></EmptyElement>"
    assert TE().markup == "<TE ></TE>"
    assert str(TE()) == "<TE ></TE>"

    assert EmptyElement(class_="test").markup == "<EmptyElement class=\"test\"></EmptyElement>"
    assert str(EmptyElement(class_="test")) == "<EmptyElement class=\"test\"></EmptyElement>"
    assert TE(class_="test").markup == "<TE class=\"test\"></TE>"
    assert str(TE(class_="test")) == "<TE class=\"test\"></TE>"

    assert EmptyElement(class_="test", **{"class": "no-test"}).markup == "<EmptyElement class=\"test\"></EmptyElement>"
    assert str(EmptyElement(class_="test", **{"class": "no-test"})) == "<EmptyElement class=\"test\"></EmptyElement>"
    assert TE(class_="test", **{"class": "no-test"}).markup == "<TE class=\"test\"></TE>"
    assert str(TE(class_="test", **{"class": "no-test"})) == "<TE class=\"test\"></TE>"

    assert EmptyElement(string="foo", int=3, float=3.1).markup == "<EmptyElement string=\"foo\" int=\"3\" float=\"3.1\"></EmptyElement>"
    assert str(EmptyElement(string="foo", int=3, float=3.1)) == "<EmptyElement string=\"foo\" int=\"3\" float=\"3.1\"></EmptyElement>"
    assert TE(string="foo", int=3, float=3.1).markup == "<TE string=\"foo\" int=\"3\" float=\"3.1\"></TE>"
    assert str(TE(string="foo", int=3, float=3.1)) == "<TE string=\"foo\" int=\"3\" float=\"3.1\"></TE>"

    assert EmptyElement(class_="cls", string="foo", int=3, float=3.1).markup == "<EmptyElement string=\"foo\" int=\"3\" float=\"3.1\" class=\"cls\"></EmptyElement>"
    assert str(EmptyElement(class_="cls", string="foo", int=3, float=3.1)) == "<EmptyElement string=\"foo\" int=\"3\" float=\"3.1\" class=\"cls\"></EmptyElement>"
    assert TE(class_="cls", string="foo", int=3, float=3.1).markup == "<TE string=\"foo\" int=\"3\" float=\"3.1\" class=\"cls\"></TE>"
    assert str(TE(class_="cls", string="foo", int=3, float=3.1)) == "<TE string=\"foo\" int=\"3\" float=\"3.1\" class=\"cls\"></TE>"

    assert EmptyElement(**{"string": "foo", "int": 3, "float": 3.1}).markup == "<EmptyElement string=\"foo\" int=\"3\" float=\"3.1\"></EmptyElement>"
    assert str(EmptyElement(**{"string": "foo", "int": 3, "float": 3.1})) == "<EmptyElement string=\"foo\" int=\"3\" float=\"3.1\"></EmptyElement>"
    assert TE(**{"string": "foo", "int": 3, "float": 3.1}).markup == "<TE string=\"foo\" int=\"3\" float=\"3.1\"></TE>"
    assert str(TE(**{"string": "foo", "int": 3, "float": 3.1})) == "<TE string=\"foo\" int=\"3\" float=\"3.1\"></TE>"

def test_SelfClosedElement():
    class TE(SelfClosedElement):
        __slots__ = ()

    assert SelfClosedElement().markup == "<SelfClosedElement />"
    assert str(SelfClosedElement()) == "<SelfClosedElement />"
    assert TE().markup == "<TE />"
    assert str(TE()) == "<TE />"

    assert SelfClosedElement(class_="test").markup == "<SelfClosedElement class=\"test\"/>"
    assert str(SelfClosedElement(class_="test")) == "<SelfClosedElement class=\"test\"/>"
    assert TE(class_="test").markup == "<TE class=\"test\"/>"
    assert str(TE(class_="test")) == "<TE class=\"test\"/>"

    assert SelfClosedElement(class_="test", **{"class": "no-test"}).markup == "<SelfClosedElement class=\"test\"/>"
    assert str(SelfClosedElement(class_="test", **{"class": "no-test"})) == "<SelfClosedElement class=\"test\"/>"
    assert TE(class_="test", **{"class": "no-test"}).markup == "<TE class=\"test\"/>"
    assert str(TE(class_="test", **{"class": "no-test"})) == "<TE class=\"test\"/>"

    assert SelfClosedElement(string="foo", int=3, float=3.1).markup == "<SelfClosedElement string=\"foo\" int=\"3\" float=\"3.1\"/>"
    assert str(SelfClosedElement(string="foo", int=3, float=3.1)) == "<SelfClosedElement string=\"foo\" int=\"3\" float=\"3.1\"/>"
    assert TE(string="foo", int=3, float=3.1).markup == "<TE string=\"foo\" int=\"3\" float=\"3.1\"/>"
    assert str(TE(string="foo", int=3, float=3.1)) == "<TE string=\"foo\" int=\"3\" float=\"3.1\"/>"

    assert SelfClosedElement(class_="cls", string="foo", int=3, float=3.1).markup == "<SelfClosedElement string=\"foo\" int=\"3\" float=\"3.1\" class=\"cls\"/>"
    assert str(SelfClosedElement(class_="cls", string="foo", int=3, float=3.1)) == "<SelfClosedElement string=\"foo\" int=\"3\" float=\"3.1\" class=\"cls\"/>"
    assert TE(class_="cls", string="foo", int=3, float=3.1).markup == "<TE string=\"foo\" int=\"3\" float=\"3.1\" class=\"cls\"/>"
    assert str(TE(class_="cls", string="foo", int=3, float=3.1)) == "<TE string=\"foo\" int=\"3\" float=\"3.1\" class=\"cls\"/>"

    assert SelfClosedElement(**{"string": "foo", "int": 3, "float": 3.1}).markup == "<SelfClosedElement string=\"foo\" int=\"3\" float=\"3.1\"/>"
    assert str(SelfClosedElement(**{"string": "foo", "int": 3, "float": 3.1})) == "<SelfClosedElement string=\"foo\" int=\"3\" float=\"3.1\"/>"
    assert TE(**{"string": "foo", "int": 3, "float": 3.1}).markup == "<TE string=\"foo\" int=\"3\" float=\"3.1\"/>"
    assert str(TE(**{"string": "foo", "int": 3, "float": 3.1})) == "<TE string=\"foo\" int=\"3\" float=\"3.1\"/>"

def test_StandaloneElement():
    class TE(StandaloneElement):
        __slots__ = ()

    assert StandaloneElement().markup == "<StandaloneElement >"
    assert str(StandaloneElement()) == "<StandaloneElement >"
    assert TE().markup == "<TE >"
    assert str(TE()) == "<TE >"

    assert StandaloneElement(class_="test").markup == "<StandaloneElement class=\"test\">"
    assert str(StandaloneElement(class_="test")) == "<StandaloneElement class=\"test\">"
    assert TE(class_="test").markup == "<TE class=\"test\">"
    assert str(TE(class_="test")) == "<TE class=\"test\">"

    assert StandaloneElement(class_="test", **{"class": "no-test"}).markup == "<StandaloneElement class=\"test\">"
    assert str(StandaloneElement(class_="test", **{"class": "no-test"})) == "<StandaloneElement class=\"test\">"
    assert TE(class_="test", **{"class": "no-test"}).markup == "<TE class=\"test\">"
    assert str(TE(class_="test", **{"class": "no-test"})) == "<TE class=\"test\">"

    assert StandaloneElement(string="foo", int=3, float=3.1).markup == "<StandaloneElement string=\"foo\" int=\"3\" float=\"3.1\">"
    assert str(StandaloneElement(string="foo", int=3, float=3.1)) == "<StandaloneElement string=\"foo\" int=\"3\" float=\"3.1\">"
    assert TE(string="foo", int=3, float=3.1).markup == "<TE string=\"foo\" int=\"3\" float=\"3.1\">"
    assert str(TE(string="foo", int=3, float=3.1)) == "<TE string=\"foo\" int=\"3\" float=\"3.1\">"

    assert StandaloneElement(class_="cls", string="foo", int=3, float=3.1).markup == "<StandaloneElement string=\"foo\" int=\"3\" float=\"3.1\" class=\"cls\">"
    assert str(StandaloneElement(class_="cls", string="foo", int=3, float=3.1)) == "<StandaloneElement string=\"foo\" int=\"3\" float=\"3.1\" class=\"cls\">"
    assert TE(class_="cls", string="foo", int=3, float=3.1).markup == "<TE string=\"foo\" int=\"3\" float=\"3.1\" class=\"cls\">"
    assert str(TE(class_="cls", string="foo", int=3, float=3.1)) == "<TE string=\"foo\" int=\"3\" float=\"3.1\" class=\"cls\">"

    assert StandaloneElement(**{"string": "foo", "int": 3, "float": 3.1}).markup == "<StandaloneElement string=\"foo\" int=\"3\" float=\"3.1\">"
    assert str(StandaloneElement(**{"string": "foo", "int": 3, "float": 3.1})) == "<StandaloneElement string=\"foo\" int=\"3\" float=\"3.1\">"
    assert TE(**{"string": "foo", "int": 3, "float": 3.1}).markup == "<TE string=\"foo\" int=\"3\" float=\"3.1\">"
    assert str(TE(**{"string": "foo", "int": 3, "float": 3.1})) == "<TE string=\"foo\" int=\"3\" float=\"3.1\">"

def test_StringElement():
    class TE(StringElement):
        __slots__ = ()

    assert StringElement("").markup == "<StringElement ></StringElement>"
    assert str(StringElement("")) == "<StringElement ></StringElement>"
    assert TE("").markup == "<TE ></TE>"
    assert str(TE("")) == "<TE ></TE>"

    assert StringElement(None).markup == "<StringElement ></StringElement>"
    assert str(StringElement(None)) == "<StringElement ></StringElement>"
    assert TE(None).markup == "<TE ></TE>"
    assert str(TE(None)) == "<TE ></TE>"

    assert StringElement("value").markup == "<StringElement >value</StringElement>"
    assert str(StringElement("value")) == "<StringElement >value</StringElement>"
    assert TE("value").markup == "<TE >value</TE>"
    assert str(TE("value")) == "<TE >value</TE>"

    assert StringElement("value", class_="cls test").markup == "<StringElement class=\"cls test\">value</StringElement>"
    assert str(StringElement("value", class_="cls test")) == "<StringElement class=\"cls test\">value</StringElement>"
    assert TE("value", class_="cls test").markup == "<TE class=\"cls test\">value</TE>"
    assert str(TE("value", class_="cls test")) == "<TE class=\"cls test\">value</TE>"

    assert StringElement("value", class_="cls", foo=42, bar="bar").markup == "<StringElement foo=\"42\" bar=\"bar\" class=\"cls\">value</StringElement>"
    assert str(StringElement("value", class_="cls", foo=42, bar="bar")) == "<StringElement foo=\"42\" bar=\"bar\" class=\"cls\">value</StringElement>"
    assert TE("value", class_="cls", foo=42, bar="bar").markup == "<TE foo=\"42\" bar=\"bar\" class=\"cls\">value</TE>"
    assert str(TE("value", class_="cls", foo=42, bar="bar")) == "<TE foo=\"42\" bar=\"bar\" class=\"cls\">value</TE>"
