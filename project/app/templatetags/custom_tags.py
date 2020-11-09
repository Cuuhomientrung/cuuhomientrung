from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from webpack_loader import utils as webpack_loader_utils
import json
from django.template.loader import get_template
from app.admin import TinhAdminFilter, HuyenAdminFilter, XaAdminFilter

register = template.Library()


def get_as_tags(bundle_name, extension=None, config='DEFAULT', attrs=''):
    bundle = webpack_loader_utils._get_bundle(bundle_name, extension, config)
    tags = []
    for chunk in bundle:
        chunk['url'] += f'?v={settings.REVISION}'
        if chunk['name'].endswith(('.js', '.js.gz')):
            tags.append((
                '<script type="text/javascript" src="{0}" {1}></script>'
            ).format(chunk['url'], attrs))
        elif chunk['name'].endswith(('.css', '.css.gz')):
            tags.append((
                '<link type="text/css" href="{0}" rel="stylesheet" {1}/>'
            ).format(chunk['url'], attrs))
    return tags


@register.simple_tag
def render_bundle(bundle_name, extension=None, config='DEFAULT', attrs=''):
    '''
    Purpose: Attach custom revision param to url
    Origin library code: https://github.com/jazzband/django-webpack-loader/blob/master/webpack_loader/templatetags/webpack_loader.py
    '''
    tags = get_as_tags(bundle_name, extension=extension, config=config, attrs=attrs)
    return mark_safe('\n'.join(tags))


@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))
@register.simple_tag
def custom_admin_list_filter(cl, spec):
    if isinstance(spec, (TinhAdminFilter, HuyenAdminFilter, XaAdminFilter)):
        spec.template = "admin/app/custom_select_filter.html"

    tpl = get_template(spec.template)
    return tpl.render({
        'title': spec.title,
        'choices': list(spec.choices(cl)),
        'spec': spec,
    })
