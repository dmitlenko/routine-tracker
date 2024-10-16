from django import forms
from django.utils.translation import gettext_lazy as _

from .models import RoutineGroup


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