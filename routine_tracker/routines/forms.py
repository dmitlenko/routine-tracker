from datetime import date

from django import forms
from django.utils.translation import gettext_lazy as _

from routine_tracker.base.utils.common import icon_choices

from .models import Routine, RoutineEntry, RoutineGroup


class RoutineGroupForm(forms.ModelForm):
    icon = forms.ChoiceField(
        choices=[('', _('None'))] + icon_choices(),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = RoutineGroup
        fields = ['name', 'description', 'icon', 'color']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _('Name')}),
            'description': forms.Textarea(attrs={'placeholder': _('Description')}),
            'color': forms.TextInput(attrs={'placeholder': _('Color'), 'type': 'color'}),
        }


class RoutineCreateForm(forms.ModelForm):
    class Meta:
        model = Routine
        fields = ['name', 'description', 'icon', 'type', 'has_goal', 'goal', 'measure']


class RoutineEntryCreateForm(forms.ModelForm):
    class Meta:
        model = RoutineEntry
        fields = ['date', 'value']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'value': date.today()}, format='%Y-%m-%d'),
            'value': forms.NumberInput(attrs={'placeholder': _('Value')}),
        }
