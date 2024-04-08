# staticjinjaplus

An opinionated sweet spot between [staticjinja](https://staticjinja.readthedocs.io/en/latest/) and a full-blown static
site generator.

![Python versions](https://img.shields.io/pypi/pyversions/staticjinjaplus.svg) ![Version](https://img.shields.io/pypi/v/staticjinjaplus.svg) ![License](https://img.shields.io/pypi/l/staticjinjaplus.svg)

[PyPI](https://pypi.org/project/staticjinjaplus/) - [Documentation](https://github.com/EpocDotFr/staticjinjaplus?tab=readme-ov-file#usage) - [Source Code](https://github.com/EpocDotFr/staticjinjaplus) - [Issue Tracker](https://github.com/EpocDotFr/staticjinjaplus/issues) - [Changelog](https://github.com/EpocDotFr/staticjinjaplus/releases)

Citing staticjinja's documentation, "most static site generators are cumbersome to use". While I fully agree, and while
I find staticjinja to be an awesome piece of software, there's still some gaps here and there that needs to be filled in
order to be able to generate a static website that will actually be ready for real world usage.

staticjinjaplus try to fill these gaps, while still being built on staticjinja and its philosophy: keep it simple, stupid.
That's also why "opinionated" is an important keyword in this project's description: choices have been made to cover some
use cases, but not all. This is not your average static site generator.

## Features

All of [staticjinja](https://staticjinja.readthedocs.io/en/latest/)'s features, plus:

> TODO

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

## Usage

> TODO

## Configuration

### `config.py`

Configuration of your project happens in a single `config.py` file in the root directory (where the `staticjinjaplus`
executable should be executed). You'll find the available configuration values below.

> [!NOTE]
>   - All paths are relative to the root directory, unless otherwise stated.
>   - None of these configuration values are required.
>   - Only uppercase variables are loaded by staticjinjaplus.

| Name             | Type                                            | Default                  | Description                                                                                                                                                                                                                                                                            |
|------------------|-------------------------------------------------|--------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `LOCALE`         | List[str]                                       | `None`                   | Locale identifiers passed to [`locale.setlocale()`](https://docs.python.org/3.12/library/locale.html#locale.setlocale) before a build is executed. The first working identifier will be used                                                                                           |
| `SERVE_PORT`     | int                                             | `8080`                   | Listening port of the HTTP server started by `staticjinjaplus serve`                                                                                                                                                                                                                   |
| `BASE_URL`       | str                                             | `http://localhost:8080/` | Protocol and domain name to use to generate meaningful absolute URLs                                                                                                                                                                                                                   |
| `MINIFY_XML`     | bool                                            | `False`                  | Enable XML and HTML minification                                                                                                                                                                                                                                                       |
| `MINIFY_JSON`    | bool                                            | `False`                  | Enable JSON minification where necessarily                                                                                                                                                                                                                                             |
| `TEMPLATES_DIR`  | str                                             | `templates`              | Directory containing the Jinja templates to be processed                                                                                                                                                                                                                               |
| `OUTPUT_DIR`     | str                                             | `output`                 | Directory where the rendered site will be saved                                                                                                                                                                                                                                        |
| `STATIC_DIR`     | str                                             | `static`                 | Directory containing static files                                                                                                                                                                                                                                                      |
| `ASSETS_DIR`     | str                                             | `assets`                 | Directory containing assets, i.e files that needs prior processing before being able to be used by the rendered site                                                                                                                                                                   |
| `ASSETS_BUNDLES` | List[Tuple[str, Tuple[str,...], Dict[str, str]] | `[]`                     | [webassets bundles](https://webassets.readthedocs.io/en/latest/bundles.html) to be registered. These are passed to [`register()`](https://webassets.readthedocs.io/en/latest/environment.html#registering-bundles). Sources are relative to `ASSETS_DIR`, destinations to `OUTPUT_DIR` |
| `CONTEXTS`       | List[Tuple[str, Any]]                           | `[]`                     | [staticjinja contexts](https://staticjinja.readthedocs.io/en/stable/user/advanced.html#loading-data) to be used by templates                                                                                                                                                           |

### Environment variables

Some configuration values may/must be overridden by environment variables of the same name when publishing your site
(`staticjinjaplus publish` command), typically in a deployment environment. You'll find the list below.

| Name          | Type   | Required?                      | Default                           | Description                                                          |
|---------------|--------|--------------------------------|-----------------------------------|----------------------------------------------------------------------|
| `BASE_URL`    | str    | Yes                            |                                   | Protocol and domain name to use to generate meaningful absolute URLs |
| `MINIFY_XML`  | bool ¹ | No, but activation recommended | `MINIFY_XML` configuration value  | Enable XML and HTML minification                                     |
| `MINIFY_JSON` | bool ¹ | No, but activation recommended | `MINIFY_JSON` configuration value | Enable JSON minification where necessarily                           |
| `SSH_USER`    | str    | Yes                            |                                   | SSH username                                                         |
| `SSH_HOST`    | str    | Yes                            |                                   | SSH hostname                                                         |
| `SSH_PORT`    | int    | No                             | `22`                              | SSH port                                                             |
| `SSH_PATH`    | str    | Yes                            |                                   | Absolute path to the deployment directory on the SSH host            |

¹ Any [falsy](https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.Boolean.falsy) or [truthy](https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.Boolean.truthy) string representation of a boolean value allowed by marshmallow

## Development

### Getting source code and installing the package with dev dependencies

  1. Clone the repository
  2. From the root directory, run: `pip install -e .[dev]` on Linux or `pip install -e ".[dev]"` on Windows

### Releasing the package

From the root directory, run `python setup.py upload`. This will build the package, create a git tag and publish on PyPI.

`__version__` in `staticjinjaplus/__version__.py` must be updated beforehand. It should adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

An associated GitHub release must be created following the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format.