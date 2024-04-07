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

## Configuration

### `config.py`

Configuration of your project happens in a single `config.py` file in the root directory. You'll find the available
configuration values below.

> [!NOTE]
> All paths are relative to the root directory, unless otherwise stated.

| Name             | Type                                            | Required? | Default                  | Description                                                                                                                                                                        |
|------------------|-------------------------------------------------|-----------|--------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `LOCALE`         | List[str]                                       | No        | `None`                   | Liste d'identifiants de locale à essayer d'appliquer avant toute génération de site. Le premier identifiant fonctionnel est utilisé.                                               |
| `SERVE_PORT`     | int                                             | No        | `8080`                   | Le port d'écoute du serveur HTTP lancé par `invoke serve`                                                                                                                          |
| `BASE_URL`       | str                                             | No        | `http://localhost:8080/` | Protocole et domaine de base pour les URLs absolues. La variable d'environnement associée est prioritaire lorsqu'elle est définie                                                  |
| `MINIFY_XML`     | bool                                            | No        | `False`                  | Minification ou non de l'XML (et par extension, de l'HTML également) résultant. La variable d'environnement associée est prioritaire lorsqu'elle est définie                       |
| `MINIFY_JSON`    | bool                                            | No        | `False`                  | Minification ou non du JSON là où c'est nécessaire. La variable d'environnement associée est prioritaire lorsqu'elle est définie                                                   |
| `TEMPLATES_DIR`  | str                                             | No        | `templates`              | Le répertoire contenant les gabarits Jinja du site                                                                                                                                 |
| `OUTPUT_DIR`     | str                                             | No        | `output`                 | Le répertoire dans lequel le site rendu sera enregistré                                                                                                                            |
| `STATIC_DIR`     | str                                             | No        | `static`                 | Le répertoire contenant tous les fichiers statiques                                                                                                                                |
| `ASSETS_DIR`     | str                                             | No        | `assets`                 | Le répertoire contenant les fichiers qui nécessitent un traitement préalable afin d'être utilisés par le site rendu                                                                |
| `ASSETS_BUNDLES` | List[Tuple[str, Tuple[str,...], Dict[str, str]] | No        | `[]`                     | Les bundles [webassets](https://webassets.readthedocs.io/en/latest/) à utiliser dans les templates (les sources sont relatives à `ASSETS_DIR`, et les destinations à `OUTPUT_DIR`) |
| `CONTEXTS`       | List[Tuple[str, Any]]                           | No        | `[]`                     | Liste de [contextes staticjinja](https://staticjinja.readthedocs.io/en/stable/user/advanced.html#loading-data) à utiliser                                                          |

### Environment variables

Some configuration values may be overridden by environment variables of the same name; also, configuration values prefixed
by `SSH_` may be set through environment variables only for security reasons. You'll find the list below.

> [!NOTE]
> These are meant for a deployment environment (that uses `staticjinjaplus publish`). While developing, you are not
> supposed to set them.

| Name          | Type                    | Required?                  | Default                           | Description                                                          |
|---------------|-------------------------|----------------------------|-----------------------------------|----------------------------------------------------------------------|
| `BASE_URL`    | str                     | Yes                        |                                   | Protocol and domain name to use to generate meaningful absolute URLs |
| `MINIFY_XML`  | str (`True` or `False`) | No, but `True` recommended | `MINIFY_XML` configuration value  | Enable XML and HTML minification                                     |
| `MINIFY_JSON` | str (`True` or `False`) | No, but `True` recommended | `MINIFY_JSON` configuration value | Enable JSON minification where necessarily                           |
| `SSH_USER`    | str                     | Yes                        |                                   | SSH username                                                         |
| `SSH_HOST`    | str                     | Yes                        |                                   | SSH hostname                                                         |
| `SSH_PORT`    | int                     | No                         | `22`                              | SSH port                                                             |
| `SSH_PATH`    | str                     | Yes                        |                                   | Absolute path to the deployment directory on the SSH host            |

## Usage

> TODO

## Development

### Getting source code and installing the package with dev dependencies

  1. Clone the repository
  2. From the root directory, run: `pip install -e .[dev]` on Linux or `pip install -e ".[dev]"` on Windows

### Releasing the package

From the root directory, run `python setup.py upload`. This will build the package, create a git tag and publish on PyPI.

`__version__` in `staticjinjaplus/__version__.py` must be updated beforehand. It should adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

An associated GitHub release must be created following the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format.