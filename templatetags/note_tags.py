from __future__ import unicode_literals
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django import template
from django.utils import importlib
from django.utils import six

from haystack.templatetags.highlight import *

register = template.Library()


class CBHighlightNode(HighlightNode, template.Node):
    def __init__(self, text_block, query, html_tag=None, css_class=None, max_length=None,title=False):
        super(CBHighlightNode,self).__init__(text_block,query,html_tag=None, css_class=None, max_length=None)
        self.title = title

    def render(self,context):
        return super(CBHighlightNode,self).render(context)

@register.tag
def cb_highlight(parser, token):
    """
    Takes a block of text and highlights words from a provided query within that
    block of text. Optionally accepts arguments to provide the HTML tag to wrap
    highlighted word in, a CSS class to use with the tag and a maximum length of
    the blurb in characters.

    Syntax::

        {% highlight <text_block> with <query> [css_class "class_name"] [html_tag "span"] [max_length 200] %}

    Example::

        # Highlight summary with default behavior.
        {% highlight result.summary with request.query %}

        # Highlight summary but wrap highlighted words with a div and the
        # following CSS class.
        {% highlight result.summary with request.query html_tag "div" css_class "highlight_me_please" %}

        # Highlight summary but only show 40 characters.
        {% highlight result.summary with request.query max_length 40 %}
    """
    bits = token.split_contents()
    tag_name = bits[0]

    if not len(bits) % 2 == 0:
        raise template.TemplateSyntaxError(u"'%s' tag requires valid pairings arguments." % tag_name)

    text_block = bits[1]

    if len(bits) < 4:
        raise template.TemplateSyntaxError(u"'%s' tag requires an object and a query provided by 'with'." % tag_name)

    if bits[2] != 'with':
        raise template.TemplateSyntaxError(u"'%s' tag's second argument should be 'with'." % tag_name)

    query = bits[3]

    arg_bits = iter(bits[4:])
    kwargs = {}

    for bit in arg_bits:
        if bit == 'css_class':
            kwargs['css_class'] = six.next(arg_bits)

        if bit == 'html_tag':
            kwargs['html_tag'] = six.next(arg_bits)

        if bit == 'max_length':
            kwargs['max_length'] = six.next(arg_bits)

        if bit == 'title':
            kwargs['title'] = six.next(arg_bits)

    return CBHighlightNode(text_block, query, **kwargs)
