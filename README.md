# markyp

Python 3 tools for creating markup documents.

## Installation

The project is listed on the Python Package Index, it can be installed simply by executing `pip install markyp`.

## Getting started

Creating new `markyp` element types is typically as simple as deriving new classes with the right name from the base elements that are provided by the project. The following example shows the creation of some HTML elements:

```Python
from markyp import ElementType
from markyp.elements import Element, StringElement

class html(Element):
    __slots__ = ()

    def __str__(self) -> str:
        return f"<!DOCTYPE html>\n{(super().__str__())}"

class head(Element):
    __slots__ = ()

class body(Element):
    __slots__ = ()

class title(StringElement):
    __slots__ = ()

class p(Element):
    __slots__ = ()

    @property
    def inline_children(self) -> bool:
        return True

class code(StringElement):
    __slots__ = ()

class ul(Element):
    __slots__ = ()

class li(Element):
    __slots__ = ()
```

Once you have defined the basic components that are required by your project, you can make document creation easier by creating higher order functions that convert your data into markup elements.

```Python
def create_unordered_list(*items: ElementType) -> ul:
    """Creates an unordered list from the received arguments."""
    return ul(
        *(li(item, class_="fancy-list-item", style="color:blue;") for item in items),
        class_="fancy-list"
    )
```

When everything is in place, a document can be created simply by instantiating the elements that make up the document. Notice that during element construction, positional arguments are treated as children elements and keyword arguments are treated as element attributes, allowing you to create documents using a markup-like syntax.

```Python
document = html(
    head(title("Hello World!")),
    body(
        p(code("markyp"), "HTML example.", style="font-weight:bold;"),
        p("Creating lists is easy as", style="color:blue;"),
        create_unordered_list("One", p("Two", style="font-style:italic;"), "Three"),
        style="font-size:20px"
    )
)
```

At this point, you have a Python object representing your document. The actual markup is created only when you convert this object into a string using either the `str()` method or the `markup` property of the element.

```Python
print(document)
```

## Domain-specific `markyp` extensions

`markyp` extensions should follow the `markyp_{domain-or-extension-name}` naming convention. Here is a list of domain-specific extensions:

- `markyp_rss`: Work in progress at https://github.com/volfpeter/markyp-rss, contribution is welcome.
- `markyp_html`: Work in progress at https://github.com/volfpeter/markyp-html, contribution is welcome.
- `markyp_highlightjs`: Work in progress at https://github.com/volfpeter/markyp-highlightjs, contribution is welcome.markyp-highlightjs
- `markyp_bootstrap4`: Work in progress at https://github.com/volfpeter/markyp-bootstrap4, contribution is welcome.

If you have created an open source `markyp` extension, please let us know and we will include your project in this list.

## Community guidelines

In general, please treat each other with respect and follow the below guidelines to interact with the project:

- _Questions, feedback_: Open an issue with a `[Question] <issue-title>` title.
- _Bug reports_: Open an issue with a `[Bug] <issue-title>` title, an adequate description of the bug, and a code snippet that reproduces the issue if possible.
- _Feature requests and ideas_: Open an issue with an `[Enhancement] <issue-title>` title and a clear description of the enhancement proposal.

## Contribution guidelines

Every form of contribution is welcome, including documentation improvements, tests, bug fixes, and feature implementations.

Please follow these guidelines to contribute to the project:

- Make sure your changes match the documentation and coding style of the project, including [PEP 484](https://www.python.org/dev/peps/pep-0484/) type annotations.
- `mypy` is used to type-check the codebase, submitted code should not produce typing errors. See [this page](http://mypy-lang.org/) for more information on `mypy`.
- _Small_ fixes can be submitted simply by creating a pull request.
- Non-trivial changes should have an associated [issue](#community-guidelines) in the issue tracker that commits must reference (typically by adding `#refs <issue-id>` to the end of commit messages).
- Please write [tests](#testing) for the changes you make (if applicable).

If you have any questions about contributing to the project, please contact the project owner.

## Testing

As mentioned in the [contribution guidelines](#contribution-guidelines), the project is type-checked using `mypy`, so first of all, the project must pass `mypy`'s static code analysis.

The project is tested using `pytest`. The chosen test layout is that tests are part of the application code, see [this page](https://docs.pytest.org/en/latest/goodpractices.html#tests-as-part-of-application-code) for details on what it means in practice.

If `pytest` is installed, the test set can be executed using the `pytest` command from within the project directory.

If `pytest-cov` is also installed, a test coverage report can be generated by executing `pytest --cov src/markyp` from the root directory of the project.

## License - MIT

The library is open-sourced under the conditions of the MIT [license](https://choosealicense.com/licenses/mit/).
