# Introduction

Citing [staticjinja](https://staticjinja.readthedocs.io/en/latest/)'s documentation, "most static site generators are cumbersome to use". While I fully agree, and while
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

## Planned features

  - Rebuild site on assets/static files change
  - Generic i18n and l10n support (powered by Babel)
