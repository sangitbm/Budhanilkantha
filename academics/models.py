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
            from .services import find_overlapping_session
            overlapping = find_overlapping_session(self.start_date, self.end_date, exclude_pk=self.pk)
            if overlapping:
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


class SchoolClass(models.Model):
    LEVEL_CHOICES = [
        ('early', 'Early Childhood'),
        ('primary', 'Primary (1-5)'),
        ('lower_secondary', 'Lower Secondary (6-8)'),
        ('secondary', 'Secondary (9-10)'),
        ('higher_secondary', 'Higher Secondary (11-12)'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=60, unique=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    stream = models.CharField(max_length=40, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    next_class = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='previous_classes',
    )

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.next_class:
            if (self.pk and self.next_class_id == self.pk) or (not self.pk and self.next_class == self):
                raise ValidationError({'next_class': 'A class cannot have itself as the next class.'})

            curr = self.next_class
            steps = 0
            while curr and steps < 30:
                if self.pk and curr.pk == self.pk:
                    raise ValidationError({'next_class': 'The promotion chain cannot form a loop.'})
                curr = curr.next_class
                steps += 1


class Section(models.Model):
    school_class = models.ForeignKey(SchoolClass, related_name='sections', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    capacity = models.PositiveSmallIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['school_class', 'name'], name='unique_section_per_class'),
        ]
        ordering = ['school_class__order', 'school_class__name', 'name']

    def __str__(self):
        return f"{self.school_class.name} - {self.name}"

