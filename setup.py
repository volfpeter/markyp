from codecs import open
from os import path
import re
from setuptools import setup, find_packages

# Get the long description from the README file
with open(path.join(path.abspath(path.dirname(__file__)), "README.md"), encoding="utf-8") as f:
    readme = f.read()

with open(path.join(path.abspath(path.dirname(__file__)), "src", "markyp", "__init__.py"), encoding="utf-8") as f:
    match = re.search("__version__ = \"(.*?)\"", f.read())
    version = match.group(1) if match else "0.0.0"

setup(
    name="markyp",
    version=version,
    description="Python 3 tools for creating markup documents.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/volfpeter/markyp",
    author="Peter Volf",
    author_email="do.volfp@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
        "Topic :: Utilities",
        "Typing :: Typed"
    ],
    keywords="markup generator utility xml html rss",
    package_dir={"": "src"},
    packages=find_packages("src", exclude=["test"]),
    python_requires=">=3.6",
    install_requires=[]
)
