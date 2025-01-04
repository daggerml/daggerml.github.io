# DaggerML Python Library

## Prerequisites

- [pipx](https://pypa.github.io/pipx/installation/)
- [hatch](https://hatch.pypa.io/latest/install/#pipx) (via `pipx`)

## Setup

Install hatch and clone [the repo][1] with submodules.

## Usage

See [the tests][2] (or example) for usage.

## Tests

```bash
hatch -e test run pytest .
```

## Build

```bash
hatch -e test run dml-build pypi
```

> [!NOTE]
> You might have to reinstall the cli with the editable flag set (e.g. `pip uninstall daggerml-cli; pip install -e ./submodules/daggerml_cli/`).

[1]: https://github.com/daggerml/python-lib/
[2]: https://github.com/daggerml/python-lib/tests/
