# Command Line Interface

The `staticjinjaplus` CLI is your main and only way to interact with staticjinjaplus. The following commands are available.

## `staticjinjaplus build`

Build the site by rendering your templates from the `TEMPLATES_DIR` directory in the `OUTPUT_DIR` directory.

It will first copy the tree contained in the `STATIC_DIR` directory in the `OUTPUT_DIR`, as-is.

staticjinja will then be initialized with the given `CONTEXTS` and Jinja's `JINJA_GLOBALS`/`JINJA_FILTERS`/`JINJA_EXTENSIONS`,
[webassets bundles](https://webassets.readthedocs.io/en/latest/bundles.html) (`WEBASSETS_BUNDLES`) will be registered, and
the actual rendering process is started.

`.html`, `.xml`, `.rss`, `.atom` and `.json` template output will be automatically minified, according to the `MINIFY_XML`
and `MINIFY_JSON` configuration values. `.md` files will be converted to HTML and rendered using the appropriate template
partial, which output will be automatically minified as well if configured so.

## `staticjinjaplus watch`

Same as `staticjinjaplus build`, except the site is rebuilt when templates are modified.

!!! note
    Assets and static files are not watched yet.

## `staticjinjaplus clean`

Delete and recreate the `OUTPUT_DIR` directory.

## `staticjinjaplus publish`

Apply configuration values override from [environment variables](configuration.md#environment-variables), then successively
run `staticjinjaplus clean` and `staticjinjaplus build`.

## `staticjinjaplus serve`

!!! warning
    It goes without saying this command is NOT meant for production use.

Serve the `OUTPUT_DIR` directory using Python's built-in HTTP server, plus a couple improvements:

  - URL rewrite for HTML files is emulated, i.e. both `/about.html` and `/about` will work
  - Custom HTTP error pages are emulated, if they are found saved as `{status code}.html` in the `OUTPUT_DIR` directory
  - The server will listen to both IPv4 *and* IPv6 loopback addresses if possible
  - RSS and Atom files will be served using the appropriate MIME type in the `Content-Type` response header

By default, you can browse your generated site at [http://localhost:8080/](http://localhost:8080/) or [http://[::1]:8080/](http://[::1]:8080/).
Port can be changed by defining `SERVE_PORT`.
