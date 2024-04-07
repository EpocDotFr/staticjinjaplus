from htmlmin import minify as minify_xml
from staticjinja import Site
from jinja2 import Template
import os


def minify_xml_template(site: Site, template: Template, **kwargs) -> None:
    """Minify XML and HTML output from a rendered Jinja template"""
    out = os.path.join(site.outpath, template.name)

    os.makedirs(os.path.dirname(out), exist_ok=True)

    with open(out, 'w', encoding=site.encoding) as f:
        f.write(
            minify_xml(
                site.get_template(template.name).render(**kwargs),
                remove_optional_attribute_quotes=False,
                remove_empty_space=True,
                remove_comments=True
            )
        )
