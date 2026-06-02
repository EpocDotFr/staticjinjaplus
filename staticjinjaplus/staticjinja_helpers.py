from staticjinjaplus import config, smart_build_url, convert_markdown_file
from htmlmin import minify as htmlmin
from staticjinja import Site, logger
from os import makedirs, path
from jinja2 import Template
from rjsmin import jsmin
from typing import Dict


def minify_xml(out: str, site: Site, template_name: str, **kwargs) -> None:
    """Render, minify and save XML template output to a file"""
    with open(out, 'w', encoding=site.encoding) as f:
        f.write(
            htmlmin(
                site.get_template(template_name).render(**kwargs),
                remove_optional_attribute_quotes=False,
                remove_empty_space=True,
                remove_comments=True
            )
        )


def minify_xml_template(site: Site, template: Template, **kwargs) -> None:
    """Minify XML output (HTML/RSS/Atom) from a rendered Jinja template"""
    out = path.join(site.outpath, template.name)

    makedirs(path.dirname(out), exist_ok=True)

    minify_xml(out, site, template.name, **kwargs)


def minify_json_template(site: Site, template: Template, **kwargs) -> None:
    """Minify JSON output from a rendered Jinja template"""
    out = path.join(site.outpath, template.name)

    makedirs(path.dirname(out), exist_ok=True)

    with open(out, 'w', encoding=site.encoding) as f:
        f.write(
            jsmin(
                site.get_template(template.name).render(**kwargs)
            )
        )


def create_markdown_file_context(template: Template) -> Dict:
    """Parse and convert a Markdown file to HTML and return the result, as well as metadata if any, to be used in the
    current context"""
    with open(path.join(config['TEMPLATES_DIR'], template.name), 'r', encoding='utf-8') as f:
        filename = path.normpath(template.name).replace('\\', '/')
        url, _ = smart_build_url(filename)
        converted, meta = convert_markdown_file(f)

        return {
            'markdown': {
                'converted': converted,
                'source': filename,
                'url': url,
                'meta': meta
            }
        }


def render_markdown_template(site: Site, template: Template, **kwargs) -> None:
    """Render a template partial from a converted Markdown file. Resulting HTML is minified as well if configured so"""
    render_template = kwargs.get('markdown', {}).get('meta', {}).get('partial', config['MARKDOWN_DEFAULT_PARTIAL'])

    if render_template in (False, 'false', 'False'):
        return
    elif render_template is None:
        logger.critical('Could not determine which template partial to use to render this Markdown template.')

        return

    render_template = render_template.lstrip('/')
    root, _ = path.splitext(template.name)
    out = path.join(site.outpath, f'{root}.html')

    makedirs(path.dirname(out), exist_ok=True)

    if config['MINIFY_XML']:
        minify_xml(out, site, render_template, **kwargs)
    else:
        site.get_template(render_template).stream(**kwargs).dump(out, encoding=site.encoding)
