from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db import models


class Task(models.Model):
    PRIORITY_LOW = 1
    PRIORITY_MEDIUM = 2
    PRIORITY_HIGH = 3
    PRIORITY_VERY_HIGH = 4
    PRIORITY = (
        (PRIORITY_LOW, _("Low")),
        (PRIORITY_MEDIUM, _("Medium")),
        (PRIORITY_HIGH, _("High")),
        (PRIORITY_VERY_HIGH, _("Very High")),
    )

    name = models.CharField(max_length=180)
    description = models.TextField(blank=True, default="")
    completed = models.BooleanField(default=False, blank=True)
    due_date = models.DateField(blank=True, null=True)
    priority = models.PositiveSmallIntegerField(
        choices=PRIORITY,
        default=PRIORITY_MEDIUM,
        blank=True,
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="assigned_tasks",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="created_tasks",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="updated_tasks",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name
