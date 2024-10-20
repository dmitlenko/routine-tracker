from datetime import date

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Routine, RoutineEntry, RoutineGroup


class RoutineGroupCreateForm(forms.ModelForm):
    class Meta:
        model = RoutineGroup
        fields = ['name', 'description', 'icon', 'color']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _('Name')}),
            'description': forms.Textarea(attrs={'placeholder': _('Description')}),
            'icon': forms.TextInput(attrs={'placeholder': _('Icon')}),
            'color': forms.TextInput(attrs={'placeholder': _('Color')}),
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
