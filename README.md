### Setup

We use [hatch](https://hatch.pypa.io/latest/install/#pipx) for environment management, so you'll need to install that.

The next step is to clone this repo and build the docs.

```bash
git clone daggerml.github.io
cd daggerml.github.io
hatch run build
```

You should see a printout saying `Seriving on http://127.0.0.1:8000` or
something like that. Go to that site and observe the docs

```{note}
The docs are built from the docstrings of the `daggerml-cli` and `daggerml` python packages on *pypi*. There are no submodules or anything yet.
```

### Misc info

* We use the [sphinx-book-theme](https://sphinx-book-theme.readthedocs.io/), so check with those docs on how to do callouts and stuff.
* We use [myst_nb](https://myst-nb.readthedocs.io/en/latest/index.html) to run jupyter notebooks.
* We use [sphinx-autobuild](https://pypi.org/project/sphinx-autobuild/) to watch files and automatically rebuild on changes for development.
* Eventually we'll keep a database around with cached executions.
* The [myst syntax cheat sheet](https://jupyterbook.org/en/stable/reference/cheatsheet.html)
