from django.utils import six
from django import template
from django.template.base import Node
from django.utils.functional import allow_lazy


register = template.Library()


@register.tag
def linebreakless(parser, token):
    nodelist = parser.parse(('endlinebreakless',))
    parser.delete_first_token()
    return LinebreaklessNode(nodelist)


class LinebreaklessNode(Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        strip_line_breaks = allow_lazy(lambda x: x.replace('\n', ''), six.text_type)
        return strip_line_breaks(self.nodelist.render(context).strip())
