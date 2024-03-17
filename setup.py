"""Setup file for the Unbored application."""

##############################################################################
# Python imports.
from pathlib    import Path
from setuptools import setup, find_packages

##############################################################################
# Import the library itself to pull details out of it.
import unbored

##############################################################################
# Work out the location of the README file.
def readme():
    """Return the full path to the README file.

    :returns: The path to the README file.
    :rtype: ~pathlib.Path
    """
    return Path( __file__).parent.resolve() / "README.md"

##############################################################################
# Load the long description for the package.
def long_desc():
    """Load the long description of the package from the README.

    :returns: The long description.
    :rtype: str
    """
    with readme().open( "r", encoding="utf-8" ) as rtfm:
        return rtfm.read()

##############################################################################
# Perform the setup.
setup(

    name                          = "unbored",
    version                       = unbored.__version__,
    description                   = str( unbored.__doc__ ),
    long_description              = long_desc(),
    long_description_content_type = "text/markdown",
    url                           = "https://github.com/davep/unbored",
    author                        = unbored.__author__,
    author_email                  = unbored.__email__,
    maintainer                    = unbored.__maintainer__,
    maintainer_email              = unbored.__email__,
    packages                      = find_packages(),
    package_data                  = { "unbored": [ "py.typed", "unbored.css" ] },
    include_package_data          = True,
    install_requires              = [ "textual=>0.52.1", "bored-api", "xdg" ],
    python_requires               = ">=3.10",
    keywords                      = "todo fun inspiration api-client terminal textual",
    entry_points                  = {
        "console_scripts": "unbored=unbored.app:run"
    },
    license                       = (
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"
    ),
    classifiers                   = [
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Environment :: Console",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Utilities",
        "Topic :: Terminals",
        "Typing :: Typed"
    ]

)

### setup.py ends here
