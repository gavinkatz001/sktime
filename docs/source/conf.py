#!/usr/bin/env python3
"""Configuration file for the Sphinx documentation builder."""

import datetime
import os
import sys

import sktime

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

ON_READTHEDOCS = os.environ.get("READTHEDOCS") == "True"
if not ON_READTHEDOCS:
    sys.path.insert(0, os.path.abspath("../.."))

# -- Project information -----------------------------------------------------
current_year = datetime.datetime.now().year
project = "sktime"
project_copyright = f"2019 - {current_year} (BSD-3-Clause License)"
author = "sktime developers"

# The full version, including alpha/beta/rc tags
CURRENT_VERSION = f"v{sktime.__version__}"

# If on readthedocs, and we're building the latest version, update tag to generate
# correct links in notebooks
if ON_READTHEDOCS:
    READTHEDOCS_VERSION = os.environ.get("READTHEDOCS_VERSION")
    if READTHEDOCS_VERSION == "latest":
        CURRENT_VERSION = "main"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.autosectionlabel",
    "numpydoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.linkcode",  # link to GitHub source code via linkcode_resolve()
    "nbsphinx",  # integrates example notebooks
    "sphinx_gallery.load_style",
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_issues",
    "sphinx.ext.doctest",
]

# Recommended by sphinx_design when using the MyST Parser
myst_enable_extensions = ["colon_fence"]

# Notebook thumbnails

# Populate thumbnails of notebooks?
nbsphinx_thumbnails = {
    "examples/02_classification": "examples/img/tsc.png",
}

# Use bootstrap CSS from theme.
panels_add_bootstrap_css = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# The main toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    ".ipynb_checkpoints",
    "Thumbs.db",
    ".DS_Store",
]

add_module_names = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# see http://stackoverflow.com/q/12206334/562769
numpydoc_show_class_members = True
# this is needed for some reason...
# see https://github.com/numpy/numpydoc/issues/69
numpydoc_class_members_toctree = False

numpydoc_validation_checks = {"all"}

# generate autosummary even if no references
autosummary_generate = True

# Members and inherited-members default to showing methods and attributes from a
# class or those inherited.
# Member-order orders the documentation in the order of how the members are defined in
# the source code.
autodoc_default_options = {
    "members": True,
    "inherited-members": True,
    "member-order": "bysource",
}

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = False

# When building HTML using the sphinx.ext.mathjax (enabled by default),
# Myst-Parser injects the tex2jax_ignore (MathJax v2) and mathjax_ignore (MathJax v3)
# classes in to the top-level section of each MyST document, and adds some default
# configuration. This ensures that MathJax processes only math, identified by the
# dollarmath and amsmath extensions, or specified in math directives. We here silence
# the corresponding warning that this override happens.
suppress_warnings = ["myst.mathjax"]

# Link to GitHub repo for github_issues extension
issues_github_path = "sktime/sktime"


def linkcode_resolve(domain, info):
    """Return URL to source code corresponding.

    Parameters
    ----------
    domain : str
    info : dict

    Returns
    -------
    url : str
    """

    def find_source():
        # try to find the file and line number, based on code from numpy:
        # https://github.com/numpy/numpy/blob/main/doc/source/conf.py#L286
        obj = sys.modules[info["module"]]
        for part in info["fullname"].split("."):
            obj = getattr(obj, part)
        import inspect
        import os

        fn = inspect.getsourcefile(obj)
        fn = os.path.relpath(fn, start=os.path.dirname(sktime.__file__))
        source, lineno = inspect.getsourcelines(obj)
        return fn, lineno, lineno + len(source) - 1

    if domain != "py" or not info["module"]:
        return None
    try:
        filename = "sktime/%s#L%d-L%d" % find_source()
    except Exception:
        filename = info["module"].replace(".", "/") + ".py"
    return f"https://github.com/sktime/sktime/blob/{CURRENT_VERSION}/{filename}"


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme = "pydata_sphinx_theme"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.

html_theme_options = {
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/sktime/sktime",
            "icon": "fab fa-github",
        },
        {
            "name": "Discord",
            "url": "https://discord.com/invite/54ACzaFsn7",
            "icon": "fab fa-discord",
        },
        {
            "name": "LinkedIn",
            "url": "https://www.linkedin.com/company/scikit-time/",
            "icon": "fab fa-linkedin",
        },
    ],
    "favicons": [
        {
            "rel": "icon",
            "sizes": "16x16",
            "href": "images/sktime-favicon.ico",
        }
    ],
    "show_prev_next": False,
    "use_edit_page_button": False,
    "navbar_start": ["navbar-logo"],
    "navbar_center": ["navbar-nav"],
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
}
html_logo = "images/sktime-logo-text-horizontal.png"
html_context = {
    "github_user": "sktime",
    "github_repo": "sktime",
    "github_version": "main",
    "doc_path": "docs/source/",
}
html_favicon = "images/sktime-favicon.ico"
html_sidebars = {
    "**": ["sidebar-nav-bs.html", "sidebar-ethical-ads.html"],
    "index": [],
    "get_started": [],
    "search": [],
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_css_files = ["css/custom.css"]

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}

html_show_sourcelink = False

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "sktimedoc"

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    # 'preamble': '',
    # Latex figure (float) alignment
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, "sktime.tex", "sktime Documentation", "sktime developers", "manual"),
]

# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "sktime", "sktime Documentation", [author], 1)]

# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "sktime",
        "sktime Documentation",
        author,
        "sktime",
        "One line description of project.",
        "Miscellaneous",
    ),
]


def _make_estimator_overview(app):
    """Make estimator overview table."""
    import pandas as pd

    from sktime.registry import all_estimators

    def _process_author_info(author_info):
        """Process author information from source code files.

        Parameters
        ----------
        author_info : str
            Author information string from source code files.

        Returns
        -------
        author_info : str
            Preprocessed author information.

        Notes
        -----
        A list of author names is turned into a string.
        Multiple author names will be separated by a comma,
        with the final name always preceded by "&".
        """
        if isinstance(author_info, str) and author_info.lower() == "sktime developers":
            link = '<a href="about/team">' "sktime developers</a>"
            return link

        if not isinstance(author_info, list):
            author_info = [author_info]

        def _add_link(github_id_str):
            link = (
                f'<a href="https://www.github.com/{github_id_str}">{github_id_str}</a>'
            )
            return link

        author_info = [_add_link(author) for author in author_info]

        if len(author_info) > 1:
            return ", ".join(author_info[:-1]) + " & " + author_info[-1]
        else:
            return author_info[0]

    # hard-coded for better user experience
    tags_by_object_type = {
        "forecaster": [
            "capability:categorical_in_X",
            "capability:insample",
            "capability:pred_int",
            "capability:pred_int:insample",
            "handles-missing-data",
            "ignores-exogeneous-X",
            "scitype:y",
            "requires-fh-in-fit",
            "X-y-must-have-same-index",
            "python_dependencies",
            "authors",
            "maintainers",
        ],
        "transformer": [
            "scitype:transform-input",
            "scitype:transform-output",
            "scitype:transform-labels",
            "capability:inverse_transform",
            "handles-missing-data",
            "capability:missing_values:removes",
            "capability:unequal_length",
            "capability:unequal_length:removes",
            "fit_is_empty",
            "transform-returns-same-time-index",
            "requires_X",
            "requires_y",
            "X-y-must-have-same-index",
            "python_dependencies",
            "authors",
            "maintainers",
        ],
        "aligner": [
            "alignment-type",
            "capability:distance",
            "capability:distance-matrix",
            "capability:missing_values",
            "capability:multiple_alignment",
            "capability:unequal_length",
            "python_dependencies",
            "authors",
            "maintainers",
        ],
        "clusterer": [
            "capability:multivariate",
            "capability:unequal_length",
            "capability:missing_values",
            "capability:contractable",
            "capability:predict",
            "capability:predict:proba",
            "capability:out_of_sample",
            "python_dependencies",
            "authors",
            "maintainers",
        ],
        "regressor": [
            "capability:multivariate",
            "capability:multioutput",
            "capability:unequal_length",
            "capability:missing_values",
            "capability:feature_importance",
            "capability:train_estimate",
            "capability:contractable",
            "python_dependencies",
            "authors",
            "maintainers",
        ],
        "classifier": [
            "capability:multivariate",
            "capability:multioutput",
            "capability:unequal_length",
            "capability:missing_values",
            "capability:feature_importance",
            "capability:train_estimate",
            "capability:contractable",
            "python_dependencies",
            "authors",
            "maintainers",
        ],
        "transformer-pairwise-panel": [
            "capability:multivariate",
            "capability:unequal_length",
            "capability:missing_values",
            "pwtrafo_type",
            "symmetric",
            "python_dependencies",
            "authors",
            "maintainers",
        ],
        "param_est": [
            "capability:multivariate",
            "capability:missing_values",
            "python_dependencies",
            "authors",
            "maintainers",
        ],
        "splitter": [
            "split_type",
            "python_dependencies",
            "authors",
            "maintainers",
        ],
        "metric": [
            "lower_is_better",
            "requires-y-train",
            "requires-y-pred-benchmark",
            "univariate-only",
            "scitype:y_pred",
            "python_dependencies",
            "authors",
            "maintainers",
        ],
        "detector": [
            "capability:multivariate",
            "capability:missing_values",
            "capability:contractable",
            "capability:predict",
            "capability:predict:proba",
            "capability:out_of_sample",
            "python_dependencies",
            "authors",
            "maintainers",
        ]
    }

    # todo: replace later by code similar to below
    # currently this retrieves too many tags
    #
    # for obj_type in tags_by_category:
    #     tag_tpl = all_tags(obj_type)
    #     tags = [tag[0] for tag in tag_tpl]
    #     tags_by_category[obj_type] = tags

    COLNAMES = [
        "Class Name",
        "Estimator Type",
        "Authors",
        "Maintainers",
        "Dependencies",
        "Import Path",
        "Tags",
    ] 

    records = []

    for obj_name, obj_class in all_estimators():
        author_tag = obj_class.get_class_tag("authors", "sktime developers")
        author_info = _process_author_info(author_tag)
        maintainer_tag = obj_class.get_class_tag("maintainers", "sktime developers")
        maintainer_info = _process_author_info(maintainer_tag)

        python_dependencies = obj_class.get_class_tag("python_dependencies", [])
        if isinstance(python_dependencies, list) and len(python_dependencies) == 1:
            python_dependencies = python_dependencies[0]

        object_types = obj_class.get_class_tag("object_type", "object")
        # the tag can contain multiple object types
        # it is a str or a lis of str - we normalize to a list
        if not isinstance(object_types, list):
            object_types = [object_types]

        # set of object types that are also in the dropdown menu
        obj_types_in_menu = list(set(object_types) & set(tags_by_object_type.keys()))

        # we populate the tags for object types that are in the dropdown
        # these will be selectable by checkboxes in the table
        tags = {}
        for object_type in obj_types_in_menu:
            for tag in tags_by_object_type[object_type]:
                tags[tag] = obj_class.get_class_tag(tag, None)

        # includes part of class string
        modpath = str(obj_class)[8:-2]
        path_parts = modpath.split(".")
        del path_parts[-2]
        clean_path = ".".join(path_parts)
        import_path = ".".join(path_parts[:-1])
        # adds html link reference
        obj_name = (
            """<a href='#'"""
            f"""onclick="go2URL('api_reference/auto_generated/{clean_path}.html',"""
            f"""'api_reference/auto_generated/{modpath}.html', event)">{obj_name}</a>"""
        )

        # determine the "main" object type
        # this is the first in the list that also appears in the dropdown menu
        # if obj_types_in_register is an empty list,
        # in which case the object will appear only in the "ALL" table
        if obj_types_in_menu == []:
            first_obj_type_in_register = object_types[0]
        else:
            first_obj_type_in_register = obj_types_in_menu[0]

        records.append(
            [
                obj_name,
                first_obj_type_in_register,
                author_info,
                maintainer_info,
                str(python_dependencies),
                import_path,
                tags,
            ]
        )

    df = pd.DataFrame(records, columns=COLNAMES)
    # with open("estimator_overview_table.md", "w") as file:
    #     df.to_markdown(file, index=False)

    with open("_static/table_all.html", "w") as file:
        df[
            ["Class Name", "Estimator Type", "Authors", "Maintainers", "Dependencies"]
        ].to_html(file, classes="pre-rendered", index=False, border=0, escape=False)

    with open("_static/estimator_overview_db.json", "w") as file:
        df.to_json(file, orient="records")
    # pass


def setup(app):
    """Set up sphinx builder.

    Parameters
    ----------
    app : Sphinx application object
    """

    def adds(pth):
        print("Adding stylesheet: %s" % pth)  # noqa: T201, T001
        app.add_css_file(pth)

    adds("fields.css")  # for parameters, etc.

    app.connect("builder-inited", _make_estimator_overview)


# -- Extension configuration -------------------------------------------------

# -- Options for nbsphinx extension ---------------------------------------
nbsphinx_execute = "never"  # always  # whether to run notebooks
nbsphinx_allow_errors = False  # False
nbsphinx_timeout = 600  # seconds, set to -1 to disable timeout

# add Binder launch button at the top
current_file = "{{ env.doc2path( env.docname, base=None) }}"

# make sure Binder points to latest stable release, not main
binder_url = f"https://mybinder.org/v2/gh/sktime/sktime/{CURRENT_VERSION}?filepath={current_file}"
nbsphinx_prolog = f"""
.. |binder| image:: https://mybinder.org/badge_logo.svg
.. _Binder: {binder_url}

|Binder|_
"""

# add link to original notebook at the bottom
notebook_url = f"https://github.com/sktime/sktime/tree/{CURRENT_VERSION}/{current_file}"
nbsphinx_epilog = f"""
----

Generated using nbsphinx_. The Jupyter notebook can be found here_.

.. _here: {notebook_url}
.. _nbsphinx: https://nbsphinx.readthedocs.io/
"""

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "python": (f"https://docs.python.org/{sys.version_info.major}", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "joblib": ("https://joblib.readthedocs.io/en/stable/", None),
    "scikit-learn": ("https://scikit-learn.org/stable/", None),
    "statsmodels": ("https://www.statsmodels.org/stable/", None),
}

# -- Options for _todo extension ----------------------------------------------
todo_include_todos = False

copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True
copybutton_line_continuation_character = "\\"
