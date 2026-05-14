from jinja2.utils import htmlsafe_json_dumps
from staticjinjaplus import config
from markupsafe import Markup
from typing import Dict


def absurl(resource: str) -> str:
    """Build an absolute URL to a file relative to the output dir"""
    return config['BASE_URL'].rstrip('/') + '/' + resource.lstrip('/')


def tojsonm(data: Dict) -> Markup:
    """Serialize the given data to JSON, minifying (or not) the output in function of current configuration"""
    return htmlsafe_json_dumps(
        data,
        indent=None if config['MINIFY_JSON'] else 4,
        separators=(',', ':') if config['MINIFY_JSON'] else None
    )


def dictmerge(left: Dict, right: Dict) -> Dict:
    """Merge two dicts"""
    return left | right
