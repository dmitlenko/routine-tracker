from typing import Union

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import OuterRef, Subquery
from django.utils.translation import gettext_lazy as _
from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_STANDARD

User = get_user_model()


class RoutineGroup(models.Model):
    """
    Routine group model.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="routine_groups", verbose_name=_("User"))
    name = models.CharField(_("Name"), max_length=100)
    description = models.TextField(_("Description"), blank=True)
    icon = models.CharField(_("Icon"), max_length=50, blank=True)
    color = models.CharField(_("Color"), max_length=7, default="#007bff")

    def get_latest_entry(self) -> Union["RoutineEntry", None]:
        """Get the latest entry for this group.

        Returns:
            Union[RoutineEntry, None]: The latest entry for the group, or None if there are no entries.
        """

        with transaction.atomic():
            latest_entry = (
                RoutineEntry.objects.filter(
                    routine=OuterRef("pk"),
                )
                .order_by("-date")
                .values("id", "date")[:1]
            )

            routines_with_latest_entry = (
                Routine.objects.filter(
                    group=self,
                )
                .annotate(
                    latest_entry_id=Subquery(latest_entry.values("id")),
                    latest_entry_date=Subquery(latest_entry.values("date")),
                )
                .select_related("group")
                .order_by("-latest_entry_date")
            )

            latest_entries = RoutineEntry.objects.filter(
                id__in=[routine.latest_entry_id for routine in routines_with_latest_entry]
            )

        if not latest_entries:
            return None

        return latest_entries.first()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = _("Routine Group")
        verbose_name_plural = _("Routine Groups")


class Routine(models.Model):
    """
    Routine model.
    """

    class Type(models.TextChoices):
        """
        Routine type choices.
        """

        CHECK = "check", _("Check")
        TIME = "time", _("Time")
        COUNT = "count", _("Count")

    class DefaultMeasures(models.TextChoices):
        """
        Routine measure choices.
        """

        SECONDS = "sec", _("Seconds")
        MINUTES = "min", _("Minutes")
        HOURS = "hrs", _("Hours")
        REPS = "rps", _("Reps")
        SETS = "sts", _("Sets")

    group = models.ForeignKey(RoutineGroup, on_delete=models.CASCADE, related_name="routines", verbose_name=_("Group"))
    name = models.CharField(_("Name"), max_length=100)
    description = MarkdownField(
        _("Description"), blank=True, rendered_field="description_rendered", validator=VALIDATOR_STANDARD
    )
    description_rendered = RenderedMarkdownField(blank=True, null=True)
    icon = models.CharField(_("Icon"), max_length=50, blank=True)

    type = models.CharField(_("Type"), max_length=5, choices=Type.choices, default=Type.CHECK)
    has_goal = models.BooleanField(_("Has a goal"), default=False)
    goal = models.PositiveIntegerField(_("Goal"), blank=True, null=True)
    measure = models.CharField(_("Measure"), max_length=50, blank=True, default=DefaultMeasures.SECONDS, null=True)

    def clean(self) -> None:
        # Check some edge cases for the routine
        # If the routine has a goal, ensure that a goal is set
        if self.has_goal and self.goal is None:
            raise ValidationError(_("A goal value must be set if the routine has a goal."))

        # If the routine has a type of 'check', ensure that it does not have a goal
        if self.type == self.Type.CHECK and self.has_goal:
            raise ValidationError(_("A check routine cannot have a goal."))

        # Call the parent class clean method
        return super().clean()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = _("Routine")
        verbose_name_plural = _("Routines")


class RoutineEntry(models.Model):
    """
    Routine entry model.
    """

    routine = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name="entries", verbose_name=_("Routine"))
    date = models.DateField(_("Date"))
    value = models.PositiveIntegerField(_("Value"))
    notes = models.TextField(_("Notes"), blank=True)

    def __str__(self):
        return f"{self.routine.name} - {self.date}"

    class Meta:
        ordering = ["-date"]
        verbose_name = _("Routine Entry")
        verbose_name_plural = _("Routine Entries")
