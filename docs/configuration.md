# Configuration

## `config.py`

Your project's configuration happens in a single `config.py` file in the root directory (where the `staticjinjaplus`
CLI should be executed). You'll find the available configuration values below.

!!! note
    - All paths are relative to the root directory, unless otherwise stated.
    - None of these configuration values are required, so is `config.py`.
    - Only uppercase variables are loaded by staticjinjaplus.

### `SERVE_PORT`

**Type:** int

**Default:** `8080`

Listening port of the HTTP server started by `staticjinjaplus serve`.

### `BASE_URL`

**Type:** str

**Default:** `http://localhost:{SERVE_PORT}/`

Protocol and domain name to use to generate meaningful absolute URLs. Set host part to `[::1]` if you plan to use IPv6.

### `MINIFY_XML`

**Type:** bool

**Default:** `False`

Enable XML minification.

### `MINIFY_JSON`

**Type:** bool

**Default:** `False`

Enable JSON minification.

### `TEMPLATES_DIR`

**Type:** str

**Default:** `templates`

Directory containing the Jinja templates to be processed.

### `OUTPUT_DIR`

**Type:** str

**Default:** `output`

Directory where the rendered site will be saved.

### `STATIC_DIR`

**Type:** str

**Default:** `static`

Directory containing static files.

### `ASSETS_DIR`

**Type:** str

**Default:** `assets`

Directory containing assets, i.e. files that needs prior processing before being able to be used by the rendered site.

### `CONTEXTS`

**Type:** List[Tuple[str, Union[Dict[str, Any], Callable]]]

**Default:** `[]`

[staticjinja contexts](https://staticjinja.readthedocs.io/en/stable/user/advanced.html#loading-data) to be used by
templates.

### `WEBASSETS_BUNDLES`

**Type:** List[Tuple[str, Tuple[str,...], Dict[str, str]]

**Default:** `[]`

[webassets bundles](https://webassets.readthedocs.io/en/latest/bundles.html) to be registered. These are passed to
[`register()`](https://webassets.readthedocs.io/en/latest/environment.html#registering-bundles). Sources are relative to
`ASSETS_DIR`, destinations to `OUTPUT_DIR`.

!!! note
    [jsmin](https://github.com/tikitu/jsmin) is already installed as dependency. It is internally used to minify JSON
    templates, and may be used in webassets bundles without any additional install step to minify Javascript files.

### `JINJA_GLOBALS`

**Type:** Dict[str, Any]

**Default:** `{}`

[jinja globals](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.globals) to be made available in all
templates.

### `JINJA_FILTERS`

**Type:** Dict[str, Callable]

**Default:** `{}`

[jinja filters](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.filters) to be made available in all
templates.

### `JINJA_EXTENSIONS`

**Type:** List[Union[str, jinja2.ext.Extension]]

**Default:** `[]`

[jinja extensions](https://jinja.palletsprojects.com/en/3.1.x/extensions/) to load.

### `MARKDOWN_EXTENSIONS`

**Type:** Dict[str, Dict]

**Default:** `{}`

[Markdown extensions](https://python-markdown.github.io/extensions/) to load and their respective configuration. Keys
are passed to [`extensions`](https://python-markdown.github.io/reference/#extensions); the entire dictionary is passed
to [`extension_configs`](https://python-markdown.github.io/reference/#extension_configs).

### `MARKDOWN_DEFAULT_PARTIAL`

**Type:** Optional[str]

**Default:** `None`

Default template partial to use when rendering Markdown files when the `partial` metadata is not present.

### `USE_HTML_EXTENSION`

**Type:** bool

**Default:** `True`

If your site's links are using URLs without `.html` extension (URL rewrite), you must set this config value to `False`.
This config value does **not** alter the behavior of `absurl()` in any way.

## Environment variables

Some configuration values may/must be overridden by environment variables **of the same name** when publishing your site
(`staticjinjaplus publish` command), typically in a deployment environment. You'll find the list below.

### `BASE_URL`

**Required:** Yes

Overrides [`BASE_URL`](#base_url).

### `MINIFY_XML`

**Required:** No, but activation recommended

Overrides [`MINIFY_XML`](#minify_xml). Must be set to any [falsy](https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.Boolean.falsy)
or [truthy](https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.Boolean.truthy) string
representation of boolean values allowed by marshmallow.

### `MINIFY_JSON`

**Required:** No, but activation recommended

Overrides [`MINIFY_JSON`](#minify_json). Must be set to any [falsy](https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.Boolean.falsy)
or [truthy](https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.Boolean.truthy) string
representation of boolean values allowed by marshmallow.

### `SSH_USER`

**Type:** str

**Required:** Yes

SSH username.

### `SSH_HOST`

**Type:** str

**Required:** Yes

SSH hostname.

### `SSH_PORT`

**Type:** int

**Required:** No

**Default:** 22

SSH port.

### `SSH_PATH`

**Type:** str

**Required:** Yes

Absolute path to the deployment directory on the SSH host.