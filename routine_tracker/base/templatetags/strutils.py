from typing import Any, Literal, Union

from django import template

register = template.Library()


@register.filter
def onlyif[T: str](value: T, arg: Any) -> Union[Literal[''], T]:
    return value if bool(arg) else ''


@register.filter
def ifnot[T: str](value: T, arg: Any) -> Union[Literal[''], T]:
    return '' if bool(arg) else value


@register.tag(name='trim')
def do_trim(parser, token):
    nodelist = parser.parse(('endtrim',))
    parser.delete_first_token()
    return TrimNode(nodelist)


class TrimNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        return self.nodelist.render(context).strip()
