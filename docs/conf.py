#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys
import datetime

import dep_builder

sys.path.insert(0, os.path.abspath(".."))

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = "4.1"


# Add any Sphinx extension module names here, as strings.
# They can be extensions coming with Sphinx (named "sphinx.ext.*") or your custom ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
]

# This value controls how to represent typehints.
autodoc_typehints = "signature"


# A dictionary for users defined type aliases that maps a type name to the full-qualified object name.
# It is used to keep type aliases not evaluated in the document.
# Defaults to empty ({}).
autodoc_type_aliases = {
    "_LoggerType": "logging.Logger",
}


# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string: source_suffix = [".rst", ".md"]
source_suffix = ".rst"


# The master toctree document.
master_doc = "index"


# General information about the project.
project = dep_builder.__name__
author = "Bas van Beek"
copyright = f"2022-{datetime.datetime.now().year}, {author}"


# The version info for the project you"re documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the built documents.
release = dep_builder.__version__  # The full version, including alpha/beta/rc tags.
version = f"{dep_builder.__version_tuple__[0]}.{dep_builder.__version_tuple__[1]}"


# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"


# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store"
]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"


# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {"includehidden": False}


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "packaging": ("https://packaging.pypa.io/en/latest/", None),
}


# True to parse NumPy style docstrings.
# False to disable support for NumPy style docstrings.
# Defaults to True.
napoleon_numpy_docstring = True


# True to use the :ivar: role for instance variables.
# False to use the .. attribute:: directive instead.
# Defaults to False.
napoleon_use_ivar = False


# True to parse NumPy style docstrings.
# False to disable support for NumPy style docstrings.
# Defaults to True.
napoleon_google_docstring = False


# True to use the .. admonition:: directive for the Example and Examples sections.
# False to use the .. rubric:: directive instead. One may look better than the other depending on what HTML theme is used.
# Defaults to False.
napoleon_use_admonition_for_examples = True


# True to use the .. admonition:: directive for Notes sections.
# False to use the .. rubric:: directive instead.
#  Defaults to False.
napoleon_use_admonition_for_notes = True


# True to use the .. admonition:: directive for References sections.
# False to use the .. rubric:: directive instead.
# Defaults to False.
napoleon_use_admonition_for_references = True

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']
