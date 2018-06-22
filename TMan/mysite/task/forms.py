from django import forms
from .models import *
from django.forms import ModelForm, HiddenInput, ModelChoiceField, DateInput

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        exclude=[""]

    def save(self, user):
        """Overriding save-form method to set current id"""
        m = super(TaskForm, self).save()
        m.author = user
        m.save()
        return m

    status = forms.ChoiceField(
        choices=Task.STATUS,
        widget=HiddenInput(),
        required=False
    )

    author = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=HiddenInput(),
        required=False
    )

    description = forms.CharField(
        label='Info',
        required=False
    )

    start_date = forms.DateField(
        widget=DateInput(attrs={'class': 'datetime-input'}),
        label='Start',
        required=False
    )
    end_date = forms.DateField(
        widget=DateInput(attrs={'class': 'datetime-input'}),
        label='End'
    )


