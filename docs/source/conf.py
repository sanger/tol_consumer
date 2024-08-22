# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
import sphinx_adc_theme

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath("../.."))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "tol-lab-share"
copyright = "2024, Sanger"
author = "Sanger"
release = "2.1.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",  # Support for Google style docstrings
    "sphinx.ext.intersphinx",  # Link to other project's documentation
    "sphinx.ext.viewcode",  # Add links to highlighted source code
    "sphinx.ext.autosummary",  # Create neat summary tables for modules/classes/functions
    "sphinx_autodoc_typehints",  # Automatically document type hints
    "sphinx.ext.todo",  # Support for todo directives
    "sphinx.ext.coverage",  # Collect documentation coverage statistics
    "sphinx.ext.githubpages",  # Publish HTML to GitHub pages
    "sphinx.ext.mathjax",  # Support for math notation via MathJax
    "sphinx.ext.ifconfig",  # Conditional inclusion of content
]

# Autodoc options
autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "private-members": True,
    "special-members": "__init__",
    "inherited-members": True,
    "show-inheritance": True,
}

templates_path = ["_templates"]
exclude_patterns = ["tol_lab_share.config"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_adc_theme'
html_theme_path = [sphinx_adc_theme.get_html_theme_path()]
html_static_path = ["_static"]
