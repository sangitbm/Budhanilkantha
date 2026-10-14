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

@register.filter
def file_ext(value):
    import os
    if not value:
        return ''
    ext = os.path.splitext(str(value))[1]
    return ext.strip('.').upper() if ext else ''

@register.filter
def bs_date(value, fmt="default"):
    if value is None:
        return ""
    import datetime
    import nepali_datetime

    if isinstance(value, str):
        try:
            value = datetime.date.fromisoformat(value)
        except (ValueError, TypeError):
            return ""
    elif isinstance(value, datetime.datetime):
        value = value.date()
    elif not isinstance(value, datetime.date):
        return ""

    try:
        bs = nepali_datetime.date.from_datetime_date(value)
    except (ValueError, OverflowError):
        return ""

    if fmt == "iso":
        return bs.strftime("%Y-%m-%d")
    return f"{bs.year} {bs.strftime('%B')} {bs.day}"
