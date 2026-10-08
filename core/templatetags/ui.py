from django import template

register = template.Library()

@register.filter
def first_word(value):
    if not value:
        return ""
    return value.split(" ")[0]

@register.filter
def rest_words(value):
    if not value:
        return ""
    words = value.split(" ")
    return " ".join(words[1:]) if len(words) > 1 else ""

@register.filter
def years_since(value):
    import datetime
    try:
        return datetime.datetime.now().year - int(value)
    except (ValueError, TypeError):
        return 0

@register.filter
def basename(value):
    if not value:
        return ''
    return str(value).split('/')[-1]
