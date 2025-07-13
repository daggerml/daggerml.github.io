# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import daggerml as dml
import dml_util  # Ensure dml_util is imported for autodoc
import daggerml_cli  # Ensure daggerml_cli is imported for autodoc
dml_util.__all__ = ("__version__", "dict_product", "tree_map")

dml.__all__ = tuple([*dml.__all__, "new", "load"])
project = "daggerml"
copyright = f"2025, Aaron Niskin and Micha Niskin | daggerml v{dml.__version__} | dml_util v{dml_util.__version__} | daggerml_cli v{daggerml_cli.__version__}"
author = "Aaron Niskin and Micha Niskin"
release = version = dml.__version__

util_version = dml_util.__version__

rst_prolog = f"""
.. |dml_version| replace:: {dml.__version__}
.. |util_version| replace:: {dml_util.__version__}
.. |cli_version| replace:: {daggerml_cli.__version__}
"""

toc_object_entries = True

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",  # Add links to highlighted source code
    "sphinx.ext.autosummary",
    # "sphinx.ext.intersphinx",
    # "myst_parser",  # For markdown support
    "myst_nb",  # For Jupyter notebooks
    # "nbsphinx",  # For Jupyter notebooks
]

# intersphinx_mapping = {
#     'daggerml': ('https://daggerml.com/python-lib/', None),
#     'daggerml_cli': ('https://daggerml.com/cli', None), 
#     'dml_util': ('https://daggerml.com/util', None),
# }

templates_path = ["_templates"]
exclude_patterns = []

# Optional: Automatically document class members
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}
autodoc_typehints = "description"
autosummary_generate = True
autosummary_imported_members = False

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_static_path = ["_static"]
html_logo = "_static/logo-nobg.png"
html_title = "DaggerML Documentation foopy"
html_show_sourcelink = False
html_sidebars = {
    "**": [
        "navbar-logo.html",
        "icon-links.html",
        "search-button-field.html",
        "sbt-sidebar-nav.html",
    ]
}

html_theme = "sphinx_book_theme"
html_theme_options = {
    "repository_url": "https://github.com/daggerml/python-lib",
    "use_repository_button": True,
    "home_page_in_toc": True,
    "show_toc_level": 2,
    "collapse_navigation": True,
    "extra_navbar": f"<div>Version: daggerml: {dml.__version__} / dml_util: {dml_util.__version__}</div>",
}

nb_custom_formats = {
    ".md": ["jupytext.reads", {"fmt": "mystnb"}],
}
myst_enable_extensions = [
    "dollarmath",
]
