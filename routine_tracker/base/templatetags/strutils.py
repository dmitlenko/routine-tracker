from typing import Any, Literal, Union

from django import template

register = template.Library()


@register.filter
def onlyif[T: str](value: T, arg: Any) -> Union[Literal[''], T]:
    return value if bool(arg) else ''
