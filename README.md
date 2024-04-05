# staticjinjaplus

An opinionated sweet spot between [staticjinja](https://staticjinja.readthedocs.io/en/latest/) and a full-blown static
site generator.

![Python versions](https://img.shields.io/pypi/pyversions/staticjinjaplus.svg) ![Version](https://img.shields.io/pypi/v/staticjinjaplus.svg) ![License](https://img.shields.io/pypi/l/staticjinjaplus.svg)

[PyPI](https://pypi.org/project/staticjinjaplus/) - [Documentation](https://github.com/EpocDotFr/staticjinjaplus#readme) - [Source Code](https://github.com/EpocDotFr/staticjinjaplus) - [Issue Tracker](https://github.com/EpocDotFr/staticjinjaplus/issues) - [Changelog](https://github.com/EpocDotFr/staticjinjaplus/releases)

Citing staticjinja's documentation, "most static site generators are cumbersome to use". While I fully agree, and while
I find staticjinja to be an awesome piece of software, there's still some gaps here and there that needs to be filled in
order to be able to generate a static website that will actually be ready for real world usage.

staticjinjaplus try to fill these gaps, while still keeping in line with staticjinja's philosophy: keep it simple, stupid.
That's also why "opinionated" is an important keyword in this project's description: choices have been made to cover 99%
use cases and there's no way to do using another manner.

## Prerequisites

  - Python >= 3.12

## Installation

From PyPI:

```bash
$ pip install staticjinjaplus
```

Locally, after cloning/downloading the repo:

```bash
$ pip install .
```

## Development

### Getting source code and installing the package with dev dependencies

  1. Clone the repository
  2. From the root directory, run: `pip install -e .[dev]` on Linux or `pip install -e ".[dev]"` on Windows

### Releasing the package

From the root directory, run `python setup.py upload`. This will build the package, create a git tag and publish on PyPI.

`__version__` in `staticjinjaplus/__version__.py` must be updated beforehand. It should adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

An associated GitHub release must be created following the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format.