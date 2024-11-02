from datetime import date

from django import forms
from django.utils.translation import gettext_lazy as _

from routine_tracker.base.utils.common import icon_choices

from .models import Routine, RoutineEntry, RoutineGroup


class RoutineGroupForm(forms.ModelForm):
    icon = forms.ChoiceField(
        choices=[("", _("None"))] + icon_choices(),
        widget=forms.Select(attrs={"class": "form-select"}),
        label=_("Icon"),
        required=False,
    )

    class Meta:
        model = RoutineGroup
        fields = ["name", "description", "icon", "color"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": _("Name")}),
            "description": forms.Textarea(attrs={"placeholder": _("Description"), "rows": 3}),
            "color": forms.TextInput(attrs={"placeholder": _("Color"), "type": "color"}),
        }


class RoutineForm(forms.ModelForm):
    icon = forms.ChoiceField(
        choices=[("", _("None"))] + icon_choices(),
        widget=forms.Select(attrs={"class": "form-select"}),
        label=_("Icon"),
        required=False,
    )

    measure = forms.CharField(
        label=_("Measure"),
        required=False,
    )

    class Meta:
        model = Routine
        fields = ["name", "description", "icon", "type", "has_goal", "goal", "measure"]
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "class": "d-none",
                    "placeholder": _("Description"),
                    "rows": 3,
                    "x-init": "new EasyMDE({element: this.$el, status: []})",
                }
            ),
        }


class RoutineEntryForm(forms.ModelForm):
    class Meta:
        model = RoutineEntry
        fields = ["date", "value", "notes"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "value": date.today()}, format="%Y-%m-%d"),
            "value": forms.NumberInput(attrs={"placeholder": _("Value")}),
        }
