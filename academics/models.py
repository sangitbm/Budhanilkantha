from django.db import models
from django.db.models import F, Q
from django.core.exceptions import ValidationError


class AcademicSession(models.Model):
    name = models.CharField(max_length=20, unique=True, help_text="For example 2083")
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']
        constraints = [
            models.UniqueConstraint(
                fields=['is_current'],
                condition=Q(is_current=True),
                name='only_one_current_session'
            ),
            models.CheckConstraint(
                condition=Q(end_date__gt=F('start_date')),
                name='session_end_after_start'
            ),
        ]

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                raise ValidationError({'end_date': 'End date must be after start date.'})
            overlapping = AcademicSession.objects.filter(
                start_date__lte=self.end_date,
                end_date__gte=self.start_date
            )
            if self.pk:
                overlapping = overlapping.exclude(pk=self.pk)
            if overlapping.exists():
                raise ValidationError("Session dates overlap with an existing session.")


class Term(models.Model):
    session = models.ForeignKey(AcademicSession, related_name='terms', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ['session', 'order']
        constraints = [
            models.UniqueConstraint(fields=['session', 'order'], name='unique_term_order_per_session'),
            models.UniqueConstraint(fields=['session', 'name'], name='unique_term_name_per_session'),
            models.CheckConstraint(condition=Q(end_date__gt=F('start_date')), name='term_end_after_start'),
        ]

    def __str__(self):
        return f"{self.session.name} - {self.name}"

    def clean(self):
        super().clean()
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                raise ValidationError({'end_date': 'End date must be after start date.'})
            try:
                session = self.session
            except AcademicSession.DoesNotExist:
                session = None
            if session and session.start_date and session.end_date:
                if self.start_date < session.start_date or self.end_date > session.end_date:
                    raise ValidationError("Term dates must lie inside its session's dates.")
