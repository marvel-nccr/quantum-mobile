# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#

# get the version from the inventory file
from pathlib import Path
import yaml

inventory = yaml.safe_load(Path("../inventory.yml").read_text())

# -- Project information -----------------------------------------------------

project = "Quantum Mobile"
copyright = "2020, NCCR MARVEL"
author = "Chris Sewell, Giovanni Pizzi, Leopold Talirz"

version = inventory["all"]["vars"]["vm_version"]
release = version

# -- General configuration ---------------------------------------------------

needs_sphinx = "2.0"
extensions = ["myst_parser", "sphinx_panels", "ablog", "sphinx.ext.intersphinx", "sphinxext.rediraffe"]

myst_enable_extensions = ["colon_fence", "deflist", "html_image"]

blog_path = "releases/index"
blog_title = "Releases"
blog_post_pattern = "releases/versions/*.md"
post_redirect_refresh = 1
post_auto_excerpt = 2
fontawesome_included = True
html_sidebars = {"releases/index": ['tagcloud.html', 'archives.html', 'sbt-sidebar-nav.html']}

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
html_title = html_short_title = f"{version}"
html_favicon = "_static/quantum-mobile-v4-text-square.png"
html_logo = "_static/quantum_mobile_text_wide.png"
html_theme_options = {
    "home_page_in_toc": True,
    "repository_url": "https://github.com/marvel-nccr/quantum-mobile",
    "repository_branch": "main",
    "use_repository_button": True,
    "use_issues_button": True,
    "path_to_docs": "docs",
    "use_edit_page_button": True,
}
panels_add_bootstrap_css = False

rediraffe_redirects = 'redirects.txt'
