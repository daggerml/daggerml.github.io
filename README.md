# Python Library

## Prerequisites

- [pipx](https://pypa.github.io/pipx/installation/)
- [hatch](https://hatch.pypa.io/latest/install/#pipx) (via `pipx`)

## Setup

Clone this repo.

```bash
git clone daggerml.github.io
cd daggerml.github.io
hatch run build
```

You should see a printout saying `Seriving on http://127.0.0.1:8000` or
something like that. Go to that site and observe the docs

> **Note:** The docs are built from the docstrings of the `daggerml-cli` and `daggerml` python packages on *pypi*. There are no submodules or anything yet.
