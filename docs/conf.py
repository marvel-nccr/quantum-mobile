# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Project information -----------------------------------------------------

project = "Quantum Mobile"
copyright = "2020, NCCR MARVEL"
author = "Chris Sewell, Giovanni Pizzi, Leopold Talirz"

version = "20.06.1"
release = "20.06.1"

# -- General configuration ---------------------------------------------------

needs_sphinx = '2.0'
extensions = ["myst_parser", "sphinx_panels"]
myst_admonition_enable = True

# The master toctree document.
master_doc = "index"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_book_theme"
html_title = f"version: {version}"
html_favicon = "static/quantum-mobile-v4-text-square.png"
html_logo = "static/quantum-mobile-v4-text-wide.svg"
html_theme_options = {
    "repository_url": "https://github.com/marvel-nccr/quantum-mobile",
    "repository_branch": "develop",
    "use_repository_button": True,
    "use_issues_button": True,
    "path_to_docs": "docs",
    "use_edit_page_button": True,
}
panels_add_bootstrap_css=False
