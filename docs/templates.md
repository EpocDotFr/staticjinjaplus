# Templates

You'll want to write your site's Jinja templates first: write them as usual. By default, staticjinjaplus searches for
Jinja templates in the `templates` directory where it is invoked. You can change that by using `TEMPLATES_DIR`.

!!! important
    Remember staticjinjaplus still stick with staticjinja's idiom: one Jinja template equal one rendered file, nothing
    more, nothing less (except for Markdown files).

!!! warning
    HTML templates which extension is not `.html` will **not** be properly handled by staticjinjaplus for the sake of
    simplicity. Please use `.html` only.

!!! note
    Jinja's [autoescape](https://jinja.palletsprojects.com/en/3.1.x/api/#autoescaping) is enabled for `.xml`, `.html`,
    `.rss` and `.atom` templates.

staticjinjaplus offers the following additional Jinja facilities.

## Globals

### `config`

**Type:** Dict[str, Any]

Configuration values loaded from [`config.py`](configuration.md#configpy) (defaults are guaranteed to be provided for
built-in values). Only uppercase variables are loaded by staticjinjaplus.

**Examples:**

```html+jinja
{{ config.BASE_URL }}         {# http://localhost:8080/ (by default) #}
{{ config.MY_CUSTOM_CONFIG }} {# Whatever you defined in your config.py (uppercase variables only) #}
```

### `absurl`

**Type:** Callable

**Signature:** `absurl(resource: str) -> str`

Build an absolute URL relative to a file located in the `OUTPUT_DIR` directory. The resource path is prefixed by
`BASE_URL`. `USE_HTML_EXTENSION` configuration value does **not** alter this function's behavior in any way: you must
provide the right resource path by yourself.

**Examples:**

```html+jinja
{# absurl() doesn't care whether an extension is given or not #}
{{ absurl('/about.html') }} {# http://localhost:8080/about.html #}
{{ absurl('/about') }}      {# http://localhost:8080/about #}
{{ absurl('about') }}       {# http://localhost:8080/about #}

{# absurl() doesn't care about whether a static file is targeted or not #}
{{ absurl('/images/logo.png') }} {# http://localhost:8080/images/logo.png #}
{{ absurl('images/logo.png') }}  {# http://localhost:8080/images/logo.png #}
```

### `embed`

**Type:** Callable

**Signature:** `embed(filename: str) -> markupsafe.Markup`

Return the file content of the given file, marked as safe to be rendered by Jinja. `filename` is relative to the
`{ASSETS_DIR}` directory. Useful to e.g embed SVG icons directly in the generated HTML.

**Examples:**

```html+jinja
{{ embed('icons/github.svg') }} {# <svg xmlns="http://www.w3.org/2000/svg" ... </svg> #}
```

### `collected`

**Type:** List[Dict[str, Any]]

List of all valid template files (as seen by staticjinja) found in the `TEMPLATES_DIR` directory. Dictionaries contained
in this list owns the following keys and values.

`source` (str)
:   The template filename.
    
    **Example:** `wow/about.html`

`type` (str)
:   The type (file extension) of the template.
    
    **Example:** `html`

`url` (str)
:   The rendered template URL.
    
    Setting `USE_HTML_EXTENSION` configuration value to `False` will remove the `.html` suffix, including for Markdown
    templates output.
    
    **Example:** `/wow/about.html`

`meta` (Dict[str, str])
:   If `type` equals `md`: metadata parsed from the source Markdown file. Multiline values have been concatenated using
    `\n` without extra spaces.
    
    **Example:** `{'my-metadata': 'any value'}`

**Examples:**

```html+jinja
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

## Filters

### `tojsonm`

**Signature**: `<data: Dict>|tojsonm -> markupsafe.Markup`

Serialize the given dictionary to a JSON string. Automatically takes into account `MINIFY_JSON` to minify (or not) the
resulting output. Useful for e.g serializing [Schema.org](https://schema.org/)'s JSON-LD-formatted data.

**Examples:**

```html+jinja
{{ dict(yes=True)|tojsonm }} {# With config['MINIFY_JSON'] == False:
                                 {
                                     "yes": true
                                 }
                             #}

{{ dict(yes=True)|tojsonm }} {# With config['MINIFY_JSON'] == True:
                                 {"yes":true}
                             #}
```

### `dictmerge`

**Signature**: `<left: Dict>\|dictmerge(right: Dict) -> Dict`

Merge two dictionaries. Does not modify existing ones, a new one will be created. Does **not** merge deeply.

**Examples:**

```html+jinja
{{ dict(yes=True)|dictmerge(dict(no=False)) }} {# {"yes": True, "no": False} #}
```

## Markdown

staticjinjaplus has generic support for working with Markdown-formatted files. Write your Markdown files (`.md`) as usual
in the `TEMPLATES_DIR` directory: they will be rendered to HTML using the appropriate template partial, and saved using
the source root pathname to the `OUTPUT_DIR` directory; i.e. `{TEMPLATES_DIR}/blog/awesome.md` will be rendered to
`{OUTPUT_DIR}/blog/awesome.html`.

!!! warning
    Markdown templates which extension is not `.md` will **not** be properly handled by staticjinjaplus for the sake of
    simplicity. Please use `.md` only.

staticjinjaplus do read metadata fields of Markdown files. Supported syntax is documented [here](https://python-markdown.github.io/extensions/meta_data/#syntax).
The only reserved metadata field is `partial`, which tells staticjinjaplus which template partial (relative to the
`TEMPLATES_DIR` directory) to use when rendering the Markdown file. See example below.

It fallbacks to `MARKDOWN_DEFAULT_PARTIAL` if the field was not found. An error will be logged if staticjinjaplus can't
determine which template partial to use, and rendering of the Markdown file will be canceled.

This template partial will be given a Markdown-specific variable named `markdown` containing a dictionary which keys and
values are detailed below.

`markdown.converted` (markupsafe.Markup)
:   The resulting HTML, marked as safe to be rendered by Jinja. Metadata are of course not included in this output.
    
    **Example:** `<p>My awesome paragraph</p>`

`markdown.source` (str)
:   The Markdown template filename.
    
    **Example:** `blog/my-article.md`

`markdown.url` (str)
:   The rendered Markdown template URL.
    
    Setting `USE_HTML_EXTENSION` configuration value to `False` will remove the `.html` suffix.
    
    **Example:** `/blog/my-article.html`

`markdown.meta` (Dict[str, str])
:   Metadata parsed from the source Markdown file. Multiline values have been concatenated using `\n` without extra spaces.
    
    **Example:** `{'my-metadata': 'any value'}`

Internal URLs must be written using the rendered version of the templates/assets/static files, i.e. URLs relative to what
will be rendered in the `OUTPUT_DIR` directory. staticjinjaplus will not rewrite any URLs in any manner: you must provide
the right ones by yourself. See example below.

See also the `collected` [Jinja global](#collected) which contain - among others - all Markdown files found in the
`TEMPLATES_DIR` directory (as seen by staticjinja) along their parsed metadata, and more.

**Example Markdown file:**

```markdown
partial: blog/_post.html

My awesome blog post. It has internal [links](/blog/my-article.html), and one image:

![](/images/attachment.png)

This image may come from the `STATIC_DIR` directory.
```
