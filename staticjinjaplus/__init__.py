from staticjinjaplus.__version__ import __version__ as staticjinjaplus_version
from staticjinja import __version__ as staticjinja_version
from typing import Dict, Any, Iterator, Tuple, Optional
from importlib import util as importlib_util
from markupsafe import Markup
from markdown import Markdown
from functools import cache
from glob import iglob
from os import path


class MarkdownWithMetadata(Markdown):
    Meta: Dict[str, Any]


_markdown_instance: Optional[MarkdownWithMetadata] = None

__generator__ = f'staticjinjaplus {staticjinjaplus_version} (staticjinja {staticjinja_version})'

# Set default config values
_serve_port = 8080

config: Dict[str, Any] = {
    'SERVE_PORT': _serve_port,
    'BASE_URL': f'http://localhost:{_serve_port}/',
    'MINIFY_XML': False,
    'MINIFY_JSON': False,
    'TEMPLATES_DIR': 'templates',
    'OUTPUT_DIR': 'output',
    'STATIC_DIR': 'static',
    'ASSETS_DIR': 'assets',
    'CONTEXTS': [],
    'WEBASSETS_BUNDLES': [],
    'WEBASSETS_CONFIG': {},
    'JINJA_GLOBALS': {},
    'JINJA_FILTERS': {},
    'JINJA_EXTENSIONS': [],
    'MARKDOWN_EXTENSIONS': {},
    'MARKDOWN_DEFAULT_PARTIAL': None,
    'USE_HTML_EXTENSION': True,
}


def load_config() -> None:
    """Load configuration from both `config.py` in the directory where staticjinjaplus is executed and environment
    variables, returning a dict representation of this configuration. Only uppercase variables are loaded"""
    global config

    # Load and override default config values from config.py, if the file exists
    try:
        spec = importlib_util.spec_from_file_location('config', 'config.py')
        actual_config = importlib_util.module_from_spec(spec)
        spec.loader.exec_module(actual_config)

        config.update({
            k: v for k, v in vars(actual_config).items() if k.isupper()
        })
    except FileNotFoundError:
        pass


def smart_build_url(filename: str) -> Tuple[str, str]:
    """Build a pretty URL (if configured so) pointing to an HTML file"""
    _, ext = path.splitext(filename)
    ext = ext.lstrip('.')

    url = '/' + filename.lstrip('/')

    if url.endswith(('/index.html', '/index.md')):
        url = url.removesuffix('/index.html').removesuffix('/index.md') + '/'
    elif ext in ('html', 'md'):
        if not config['USE_HTML_EXTENSION']:
            url, _ = path.splitext(url)
        elif ext == 'md':
            url, = url.removesuffix('.md') + '.html'

    return url, ext


@cache
def collect_templates() -> Iterator[Dict[str, Any]]:
    """Iterates over all valid files found in the templates directory and return several kind of information about
    them."""
    for filename in iglob(
        f'**/[!_]*.*',
        root_dir=config['TEMPLATES_DIR'],
        recursive=True
    ):
        filename = path.normpath(filename).replace('\\', '/')

        url, ext = smart_build_url(filename)

        data = {
            'source': filename,
            'type': ext,
            'url': url,
        }

        if ext == 'md':
            with open(path.join(config['TEMPLATES_DIR'], filename), 'r', encoding='utf-8') as f:
                converted, meta = convert_markdown_file(f)

                data['meta'] = meta

                if meta.get('partial', config['MARKDOWN_DEFAULT_PARTIAL']) is False:
                    data['converted'] = converted

        yield data


def convert_markdown_file(f) -> Tuple[Markup, Dict]:
    global _markdown_instance

    # Use a single Markdown parser instance for performance reasons
    if not _markdown_instance:
        extension_configs = {
            'markdown.extensions.extra': {},
            'markdown.extensions.meta': {},
        }

        if config['MARKDOWN_EXTENSIONS']:
            extension_configs.update(config['MARKDOWN_EXTENSIONS'])

        extensions = [
            e for e in extension_configs.keys()
        ]

        _markdown_instance = MarkdownWithMetadata(
            extensions=extensions,
            extension_configs=extension_configs,
            output_format='html5'
        )
    else:  # Reset the Markdown parser state before reusing it
        _markdown_instance.reset()

    return (
        Markup(_markdown_instance.convert(f.read())),
        {
            k: '\n'.join(v) for k, v in _markdown_instance.Meta.items()
        }
    )


load_config()
