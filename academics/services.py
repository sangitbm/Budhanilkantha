import datetime
import re
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
import nepali_datetime

from .models import AcademicSession, Term

_MISSING = object()


class SessionOverlapError(ValidationError):
    pass


@transaction.atomic
def set_current_session(session):
    AcademicSession.objects.filter(is_current=True).exclude(pk=session.pk).update(is_current=False)
    session.is_current = True
    session.save()
    cache.delete('current_session')
    return session


def next_session_name(name):
    clean_name = name.strip()
    m_range = re.match(r"^(\d+)/(\d+)$", clean_name)
    m_single = re.match(r"^(\d+)$", clean_name)
    if m_range:
        first, second = m_range.groups()
        next_first = str(int(first) + 1)
        next_second = str(int(second) + 1).zfill(len(second))
        base_name = f"{next_first}/{next_second}"
    elif m_single:
        base_name = str(int(m_single.group(1)) + 1)
    else:
        base_name = f"{clean_name} (copy)"

    candidate = base_name
    counter = 2
    while AcademicSession.objects.filter(name=candidate).exists():
        candidate = f"{base_name} ({counter})"
        counter += 1
    return candidate


def find_overlapping_session(start, end, exclude_pk=None):
    if not (start and end):
        return None
    qs = AcademicSession.objects.filter(
        start_date__lte=end,
        end_date__gte=start
    )
    if exclude_pk:
        qs = qs.exclude(pk=exclude_pk)
    return qs.first()


@transaction.atomic
def duplicate_session(session):
    name = next_session_name(session.name)
    try:
        bs = nepali_datetime.date.from_datetime_date(session.start_date)
        next_bs = nepali_datetime.date(bs.year + 1, bs.month, bs.day)
        new_start = next_bs.to_datetime_date()
    except (ValueError, OverflowError):
        new_start = session.start_date + datetime.timedelta(days=365)

    delta = new_start - session.start_date
    new_end = session.end_date + delta

    overlapping = find_overlapping_session(new_start, new_end)
    if overlapping:
        raise SessionOverlapError(f"An academic year already covers these dates: {overlapping.name}.")

    new_session = AcademicSession.objects.create(
        name=name,
        start_date=new_start,
        end_date=new_end,
        is_current=False,
    )

    for term in session.terms.all().order_by('order'):
        Term.objects.create(
            session=new_session,
            name=term.name,
            start_date=term.start_date + delta,
            end_date=term.end_date + delta,
            order=term.order,
        )

    return new_session


def default_session_dates(today=None):
    if today is None:
        today = timezone.localdate()
    try:
        bs = nepali_datetime.date.from_datetime_date(today)
        name = str(bs.year)
        start = nepali_datetime.date(bs.year, 1, 1).to_datetime_date()
        next_start = nepali_datetime.date(bs.year + 1, 1, 1).to_datetime_date()
        end = next_start - datetime.timedelta(days=1)
        return (name, start, end)
    except (ValueError, OverflowError):
        name = str(today.year)
        start = datetime.date(today.year, 1, 1)
        end = datetime.date(today.year, 12, 31)
        return (name, start, end)


def get_current_session():
    cached = cache.get('current_session', _MISSING)
    if cached is not _MISSING:
        return cached
    session = AcademicSession.objects.filter(is_current=True).first()
    cache.set('current_session', session, 300)
    return session


def suggest_terms(start, end, names=("First Terminal", "Second Terminal", "Final Terminal")):
    k = len(names)
    if k == 0:
        return []
    total_days = (end - start).days + 1
    terms = []
    current_start = start
    for i, name in enumerate(names):
        order = i + 1
        if i == k - 1:
            term_end = end
        else:
            target_days = round((i + 1) * total_days / k)
            term_end = start + datetime.timedelta(days=target_days - 1)
        terms.append({
            'name': name,
            'start_date': current_start,
            'end_date': term_end,
            'order': order,
        })
        current_start = term_end + datetime.timedelta(days=1)
    return terms


def get_current_term(session, today=None):
    if not session:
        return None
    if today is None:
        today = timezone.localdate()
    return session.terms.filter(start_date__lte=today, end_date__gte=today).first()


def days_left(end_date, today=None):
    if today is None:
        today = timezone.localdate()
    diff = (end_date - today).days
    return max(0, diff)
