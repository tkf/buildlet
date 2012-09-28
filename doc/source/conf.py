# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.abspath('../..'))

# -- General configuration ----------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.inheritance_diagram',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'buildlet'
copyright = u'2012, Takafumi Arakaki'

# The short X.Y version.
version = '0'
# The full version, including alpha/beta/rc tags.
release = '0'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output --------------------------------------------------

html_theme = 'default'

html_theme_options = {
    'nosidebar': True,
}

html_static_path = []  # default: ['_static']

# Output file base name for HTML help builder.
htmlhelp_basename = 'buildletdoc'


# -- Options for LaTeX output -------------------------------------------------

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
#'papersize': 'letterpaper',

# The font size ('10pt', '11pt' or '12pt').
#'pointsize': '10pt',

# Additional stuff for the LaTeX preamble.
#'preamble': '',
}

# Grouping the document tree into LaTeX files. List of tuples
latex_documents = [
    ('index',                    # source start file
     'buildlet.tex',             # target name
     u'buildlet Documentation',  # title
     u'Takafumi Arakaki',        # author
     'manual'),                  # documentclass [howto/manual]
]


# -- Options for manual page output -------------------------------------------

# One entry per manual page. List of tuples
man_pages = [
    ('index',                    # source start file
     'buildlet',                 # name
     u'buildlet Documentation',  # description
     [u'Takafumi Arakaki'],      # authors
     1)                          # manual section
]


# -- Options for Texinfo output -----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
texinfo_documents = [
  ('index',                                             # source start file
   'buildlet',                                          # target name
   u'buildlet Documentation',                           # title
   u'Takafumi Arakaki',                                 # author
   'buildlet',                                          # dir menu entry
   'build tool like functionality as a Python module',  # description,
   'Miscellaneous'),                                    # category
]


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'http://docs.python.org/': None}

autodoc_member_order = 'bysource'

inheritance_graph_attrs = dict(rankdir="TB")
