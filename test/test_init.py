import pytest

from markyp import IElement, is_element

def test_IElement():
    with pytest.raises(NotImplementedError):
        str(IElement())

    with pytest.raises(NotImplementedError):
        IElement().markup

def test_is_element():
    assert is_element(IElement())
    assert is_element("string element")
    assert not is_element(b"not a string element")
    assert not is_element(42)
    assert not is_element({})
    assert not is_element([])
    assert not is_element(True)
    assert not is_element(None)
