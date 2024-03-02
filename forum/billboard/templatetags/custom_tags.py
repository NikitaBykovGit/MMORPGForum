from django import template

from billboard.models import Response

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()


@register.simple_tag(takes_context=True)
def get_count_responses(context, **kwargs):
    responses = Response.objects.filter(post__author=context['user'], status=False)
    return responses.count()