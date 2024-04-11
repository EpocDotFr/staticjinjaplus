# staticjinjaplus

A sweet spot between [staticjinja](https://staticjinja.readthedocs.io/en/latest/) and a full-blown static  site generator.

![Python versions](https://img.shields.io/pypi/pyversions/staticjinjaplus.svg) ![Version](https://img.shields.io/pypi/v/staticjinjaplus.svg) ![License](https://img.shields.io/pypi/l/staticjinjaplus.svg)

[PyPI](https://pypi.org/project/staticjinjaplus/) - [Documentation](https://github.com/EpocDotFr/staticjinjaplus?tab=readme-ov-file#readme) - [Source Code](https://github.com/EpocDotFr/staticjinjaplus) - [Issue Tracker](https://github.com/EpocDotFr/staticjinjaplus/issues) - [Changelog](https://github.com/EpocDotFr/staticjinjaplus/releases)

Citing staticjinja's documentation, "most static site generators are cumbersome to use". While I fully agree, and while
I find staticjinja to be an awesome piece of software, there's still some gaps here and there that needs to be filled in
order to be able to generate a static website that will actually be ready for real world usage.

staticjinjaplus try to fill these gaps, while still being built on staticjinja and its philosophy: keep it simple, stupid.
Note staticjinjaplus is opinionated: choices have been made to cover some use cases, but not all. This is not your average
static site generator.

## Features

All of [staticjinja](https://staticjinja.readthedocs.io/en/latest/)'s features, plus:

  - Simple, file-based configuration to centralize *a handful* of configuration values
  - Generic Markdown support (**not** your usual "pages" or "articles/blog posts" feature)
  - Build improvements
    - Automatically copy static files to output directory
    - Define Jinja and staticjinja initialization parameters in a config file
    - Define [webassets](https://webassets.readthedocs.io/en/latest/) bundles to allow CSS/JS concatenation/minification
    - Automatically minify XML (including HTML, RSS and Atom)/JSON output
  - Jinja improvements
    - A few new Jinja globals/filters to make your life easier
    - Autoescape is enabled for XML, HTML, RSS and Atom templates
  - Serve the generated site through a local HTTP server
    - URL rewrite emulation (for HTML files)
    - Custom HTTP error pages emulation
    - IPv6 loopback address support
    - Serve proper MIME type for RSS and Atom files
  - Publish the generated site through rsync over SSH

**Planned:**

  - Rebuild site on assets/static files change
  - Generic i18n and l10n support (powered by Babel)

## Prerequisites

  - Python >= 3.10

## Installation

From PyPI:

```bash
$ pip install staticjinjaplus
```

Locally, after cloning/downloading the repo:

```bash
$ pip install .
```

A CLI (`staticjinjaplus`) will be made available upon installation.

## Usage

### Templates

You'll want to write your site's Jinja templates first: write them as usual. By default, staticjinjaplus searches for
Jinja templates in the `templates` directory where it is invoked. You can change that by using the `TEMPLATES_DIR`
[configuration value](#configpy).

Remember staticjinjaplus still stick with staticjinja's idiom: one Jinja template equal one rendered file, nothing more,
nothing less.

> [!WARNING]
> HTML templates which extension is not `.html` will **not** be properly handled by staticjinjaplus for the sake of
> simplicity. Please use `.html` only.

staticjinjaplus offers the following additional Jinja facilities.

#### Globals

| Name/signature                              | Type                 | Description                                                                                                                                                                                                                         |
|---------------------------------------------|----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `config`                                    | Dict[str, Any]       | Configuration values loaded from [`config.py`](#configpy) (defaults are guaranteed to be provided for built-in values). Only uppercase variables are loaded by staticjinjaplus                                                      |
| `absurl(resource: str) -> str`              | Callable             | Build an absolute URL relative to a file located in the `OUTPUT_DIR` directory. The resource path is prefixed by `BASE_URL` (see [configuration values](#configpy))                                                                 |
| `embed(filename: str) -> markupsafe.Markup` | Callable             | Return the file content of the given file, marked as safe to be rendered by Jinja. `filename` is relative to the `{ASSETS_DIR}` directory. Useful to e.g embed SVG icons directly in the generated HTML                             |
| `collected`                                 | List[Dict[str, Any]] | List of all valid template files (as seen by staticjinja) found in the `TEMPLATES_DIR` directory. Dictionary include source filename, rendered template URL, file extension, and for Markdown (`.md`) files their parsed metadata. |

**Usage examples:**

```html+jinja
{{ config.BASE_URL }}         {# http://localhost:8080/ (by default) #}
{{ config.MY_CUSTOM_CONFIG }} {# Whatever you defined in your config.py (uppercase variables only) #}

{# absurl() doesn't care whether an extension is given or not #}
{{ absurl('/about.html') }} {# http://localhost:8080/about.html #}
{{ absurl('/about') }}      {# http://localhost:8080/about #}
{{ absurl('about') }}       {# http://localhost:8080/about #}

{# absurl() doesn't care about whether a static file is targeted or not #}
{{ absurl('/images/logo.png') }} {# http://localhost:8080/images/logo.png #}
{{ absurl('images/logo.png') }}  {# http://localhost:8080/images/logo.png #}

{{ embed('icons/github.svg') }} {# <svg xmlns="http://www.w3.org/2000/svg" ... </svg> #}

{{ collected }}
{#
    [
      {'source': 'index.html', 'type': 'html', url': '/'},
      {'source': 'site/about.html', 'type': 'html', 'url': '/site/about.html'},
      {'source': 'categories/index.html', 'type': 'html', 'url': '/categories/'},
      {'source': 'woah.md', 'type': 'md', 'url': '/woah.html', 'meta': { ... }},
      {'source': 'index.md', 'type': 'md', 'url': '/', 'meta': { ... }},
      {'source': 'blog/an-article.md', 'type': 'md', 'url': '/blog/an-article.html', 'meta': { ... }},
      {'source': 'blog/index.md', 'type': 'md', 'url': '/blog/', 'meta': { ... }}
    ]
#}
```

#### Filters

| Signature                                      | Description                                                                                                                                                                                                                                                         |
|------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `<data: Dict>\|tojsonm -> markupsafe.Markup`   | Serialize the given dictionary to a JSON string. Automatically takes into account the `MINIFY_JSON` [configuration value](#configpy) to minify (or not) the resulting output. Useful for e.g serializing [Schema.org](https://schema.org/)'s JSON-LD-formatted data |
| `<left: Dict>\|dictmerge(right: Dict) -> Dict` | Merge two dictionaries. Does not modify existing ones, a new one will be created. Does **not** merge deeply                                                                                                                                                         |

**Usage examples:**

```html+jinja
{{ dict(yes=True)|tojsonm }} {# With config['MINIFY_JSON'] == False:
                                 {
                                     "yes": true
                                 }
                             #}

{{ dict(yes=True)|tojsonm }} {# With config['MINIFY_JSON'] == True:
                                 {"yes":true}
                             #}

{{ dict(yes=True)|dictmerge(dict(no=False)) }} {# {"yes": True, "no": False} #}
```

#### Markdown

> [!WARNING]
> Markdown templates which extension is not `.md` will **not** be properly handled by staticjinjaplus for the sake of
> simplicity. Please use `.md` only.

staticjinjaplus has generic support for working with Markdown-formatted files. Write your Markdown files (`.md`) as usual
in the `TEMPLATES_DIR` directory: they will be rendered to HTML using the appropriate template partial, and saved using
the source root pathname to the `OUTPUT_DIR` directory; i.e. `{TEMPLATES_DIR}/blog/awesome.md` will be rendered to
`{OUTPUT_DIR}/blog/awesome.html`.

staticjinjaplus do read metadata fields of Markdown files. Supported syntax is documented [here](https://python-markdown.github.io/extensions/meta_data/#syntax).
The only reserved metadata field is `partial`, which tells staticjinjaplus which template partial (relative to the
`TEMPLATES_DIR` directory) to use when rendering the Markdown file. See example below.

It fallbacks to the `MARKDOWN_DEFAULT_PARTIAL` [configuration value](#configpy) if the field was not found. An error will
be logged if staticjinjaplus can't determine which template partial to use, and rendering of the Markdown file will be
canceled.

This template partial will be given a Markdown-specific variable named `markdown` containing a dictionary which keys and
values are detailed below.

| Name                 | Type              | Description                                                                                                            |
|----------------------|-------------------|------------------------------------------------------------------------------------------------------------------------|
| `markdown.converted` | markupsafe.Markup | The resulting HTML, marked as safe to be rendered by Jinja. Metadata are of course not included in this output         |
| `markdown.source`    | str               | The Markdown template filename                                                                                         |
| `markdown.url`       | str               | The rendered Markdown template URL                                                                                     |
| `markdown.meta`      | Dict[str, str]    | Metadata parsed from the source Markdown file. Multiline values have been concatenated using `\n` without extra spaces |

Internal URLs must be written using the rendered version of the templates/assets/static files, i.e. URLs relative to what
will be rendered in the `OUTPUT_DIR` directory. staticjinjaplus will not rewrite any URLs in any manner: you must provide
the right ones by yourself. See example below.

See also the `collected` [Jinja global](#globals) which contain - among others - all Markdown files found in the
`TEMPLATES_DIR` directory (as seen by staticjinja) along their parsed metadata, and more.

**Example Markdown file:**

```markdown
partial: blog/_post.html

My awesome blog post. It has internal [links](/blog/my-article.html), and one image:

![](/images/attachment.png)

This image may come from the `STATIC_DIR` directory.
```

### Command line interface

The `staticjinjaplus` CLI is your main and only way to interact with staticjinjaplus. The following commands are available.

#### `staticjinjaplus build`

Build the site by rendering your templates from the `TEMPLATES_DIR` directory in the `OUTPUT_DIR` directory.

**Options:**

  - `-w, --watch` Automatically rebuild the site when templates are modified. **This option does not watch for assets or static files changes (yet?)**

It will then copy the tree contained in the `STATIC_DIR` directory in the `OUTPUT_DIR`, as-is.

staticjinja will be then initialized with the given `CONTEXTS` and Jinja's `JINJA_GLOBALS`/`JINJA_FILTERS`/`JINJA_EXTENSIONS`,
[webassets bundles](https://webassets.readthedocs.io/en/latest/bundles.html) (`WEBASSETS_BUNDLES`) will be registered, and
the actual rendering process is started.

`.html`, `.xml`, `.rss`, `.atom` and `.json` template output will be automatically minified, according to the `MINIFY_XML`
and `MINIFY_JSON` configuration values. `.md` files will be converted to HTML and rendered using the appropriate template
partial, which output will be automatically minified as well if configured so.

#### `staticjinjaplus clean`

Delete and recreate the `OUTPUT_DIR` directory.

#### `staticjinjaplus publish`

> [!NOTE]
> This feature requires a Linux-like environment.

Apply configuration values override from [environment variables](#environment-variables), then successively run
`staticjinjaplus clean` and `staticjinjaplus build` prior remotely syncing the `OUTPUT_DIR` directory content using
`rsync` through SSH.

#### `staticjinjaplus serve`

Serve the `OUTPUT_DIR` directory using Python's built-in HTTP server, plus a couple improvements:

  - URL rewrite for HTML files is emulated, i.e. both `/about.html` and `/about` will work
  - Custom HTTP error pages are emulated, if they are found saved as `{status code}.html` in the output directory
  - The server will listen to both IPv4 *and* IPv6 loopback addresses if possible
  - RSS and Atom files will be served using the appropriate MIME type in the `Content-Type` response header

By default, you can browse your generated site at http://localhost:8080/ or [http://[::1]:8080/](http://[::1]:8080/).
Port can be changed by defining the `SERVE_PORT` [configuration value](#configpy).

## Configuration

### `config.py`

Your project's configuration happens in a single `config.py` file in the root directory (where the `staticjinjaplus`
CLI should be executed). You'll find the available configuration values below.

> [!NOTE]
>   - All paths are relative to the root directory, unless otherwise stated.
>   - None of these configuration values are required, so is `config.py`.
>   - Only uppercase variables are loaded by staticjinjaplus.

| Name                       | Type                                              | Default                          | Description                                                                                                                                                                                                                                                                                                                           |
|----------------------------|---------------------------------------------------|----------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `SERVE_PORT`               | int                                               | `8080`                           | Listening port of the HTTP server started by `staticjinjaplus serve`                                                                                                                                                                                                                                                                  |
| `BASE_URL`                 | str                                               | `http://localhost:{SERVE_PORT}/` | Protocol and domain name to use to generate meaningful absolute URLs. Set host part to `[::1]` if you plan to use IPv6                                                                                                                                                                                                                |
| `MINIFY_XML`               | bool                                              | `False`                          | Enable XML minification                                                                                                                                                                                                                                                                                                               |
| `MINIFY_JSON`              | bool                                              | `False`                          | Enable JSON minification                                                                                                                                                                                                                                                                                                              |
| `TEMPLATES_DIR`            | str                                               | `templates`                      | Directory containing the Jinja templates to be processed                                                                                                                                                                                                                                                                              |
| `OUTPUT_DIR`               | str                                               | `output`                         | Directory where the rendered site will be saved                                                                                                                                                                                                                                                                                       |
| `STATIC_DIR`               | str                                               | `static`                         | Directory containing static files                                                                                                                                                                                                                                                                                                     |
| `ASSETS_DIR`               | str                                               | `assets`                         | Directory containing assets, i.e. files that needs prior processing before being able to be used by the rendered site                                                                                                                                                                                                                 |
| `CONTEXTS`                 | List[Tuple[str, Union[Dict[str, Any], Callable]]] | `[]`                             | [staticjinja contexts](https://staticjinja.readthedocs.io/en/stable/user/advanced.html#loading-data) to be used by templates                                                                                                                                                                                                          |
| `WEBASSETS_BUNDLES`        | List[Tuple[str, Tuple[str,...], Dict[str, str]]   | `[]`                             | [webassets bundles](https://webassets.readthedocs.io/en/latest/bundles.html) to be registered. These are passed to [`register()`](https://webassets.readthedocs.io/en/latest/environment.html#registering-bundles). Sources are relative to `ASSETS_DIR`, destinations to `OUTPUT_DIR`                                                |
| `JINJA_GLOBALS`            | Dict[str, Any]                                    | `{}`                             | [jinja globals](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.globals) to be made available in all templates                                                                                                                                                                                                     |
| `JINJA_FILTERS`            | Dict[str, Callable]                               | `{}`                             | [jinja filters](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.filters) to be made available in all templates                                                                                                                                                                                                     |
| `JINJA_EXTENSIONS`         | List[Union[str, jinja2.ext.Extension]]            | `[]`                             | [jinja extensions](https://jinja.palletsprojects.com/en/3.1.x/extensions/) to load                                                                                                                                                                                                                                                    |
| `MARKDOWN_EXTENSIONS`      | Dict[str, Dict]                                   | `{}`                             | [Markdown extensions](https://python-markdown.github.io/extensions/) to load and their respective configuration. Keys are passed to [`extensions`](https://python-markdown.github.io/reference/#extensions); the entire dictionary is passed to [`extension_configs`](https://python-markdown.github.io/reference/#extension_configs) |
| `MARKDOWN_DEFAULT_PARTIAL` | Optional[str]                                     | `None`                           | Default template partial to use when rendering Markdown files when the `partial` metadata is not present                                                                                                                                                                                                                              |
| `USE_HTML_EXTENSION`       | bool                                              | `True`                           | If your site's links are using URLs without `.html` extension (URL rewrite), you must set this config value to `False`. This config value does **not** alter the behavior of `absurl()` in any way                                                                                                                                    |

### Environment variables

Some configuration values may/must be overridden by environment variables of the same name when publishing your site
(`staticjinjaplus publish` command), typically in a deployment environment. You'll find the list below.

| Name          | Type   | Required?                      | Default                           | Description                                                          |
|---------------|--------|--------------------------------|-----------------------------------|----------------------------------------------------------------------|
| `BASE_URL`    | str    | Yes                            |                                   | Protocol and domain name to use to generate meaningful absolute URLs |
| `MINIFY_XML`  | bool ¹ | No, but activation recommended | `MINIFY_XML` configuration value  | Enable XML minification                                              |
| `MINIFY_JSON` | bool ¹ | No, but activation recommended | `MINIFY_JSON` configuration value | Enable JSON minification                                             |
| `SSH_USER`    | str    | Yes                            |                                   | SSH username                                                         |
| `SSH_HOST`    | str    | Yes                            |                                   | SSH hostname                                                         |
| `SSH_PORT`    | int    | No                             | `22`                              | SSH port                                                             |
| `SSH_PATH`    | str    | Yes                            |                                   | Absolute path to the deployment directory on the SSH host            |

¹ Any [falsy](https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.Boolean.falsy) or
[truthy](https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.Boolean.truthy) string
representation of boolean values allowed by marshmallow

## Development

### Getting source code and installing the package with dev dependencies

  1. Clone the repository
  2. From the root directory, run: `pip install -e .[dev]` on Linux or `pip install -e ".[dev]"` on Windows

### Releasing the package

From the root directory, run `python setup.py upload`. This will build the package, create a git tag and publish on PyPI.

`__version__` in `staticjinjaplus/__version__.py` must be updated beforehand. It should adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

An associated GitHub release must be created following the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format.