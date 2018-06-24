from django import forms
from .models import *

from django.forms import ModelForm, HiddenInput, ModelChoiceField, DateInput


class SchedulerForm(forms.ModelForm):

    class Meta:
        model = SchedulerModel
        exclude = [""]


    def save(self, user):
        """Overriding save-form method to set current id"""
        m = super(SchedulerForm, self).save()
        m.author = user
        m.save()
        return m


    last_added = forms.DateTimeField(
        widget=HiddenInput(),
        required=False
    )

    subscribers = forms.MultipleChoiceField(
        widget=HiddenInput(),
        required=False)

    author = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=HiddenInput(),
        required=False)

    status = forms.ChoiceField(
        choices=Task.STATUS,
        widget=HiddenInput(),
        required=False)

    start_date = forms.DateField(
        widget=DateInput(attrs={'class': 'datetime-input'}),
        label='Start',
        required=False)

    end_date = forms.DateField(
        widget=DateInput(attrs={'class': 'datetime-input'}),
        label='End')


class TaskForm(forms.ModelForm):
    """Class describing form of Task's adding"""

    class Meta:
        model = Task
        exclude = [""]

    def save(self, user):
        """Overriding save-form method to set current id"""
        m = super(TaskForm, self).save()
        m.author = user
        m.save()
        m.subscribers.add(user)
        m.save()
        return m

    # region Form fields settings
    title = forms.CharField(widget=forms.TextInput(attrs={'size':20, 'maxlength':20}))
    subscribers = forms.MultipleChoiceField(
    widget=HiddenInput(),
        required=False
    )

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

    # endregion


class TaskShareForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ["author",
                   "title",
                   "description",
                   "start_date",
                   "end_date",
                   "tag",
                   "priority",
                   "parent",
                   "status"
                   ]

    def save(self, user):
        """Overriding save-form method to set current id"""
        m = super(TaskShareForm, self).save()
        m.author = user
        m.save()
        m.subscribers.add(user)
        m.save()
        return m



class SubtaskAddForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ["parent"]

    def save(self, user, parent):
        """Overriding save-form method to set current id"""
        m = super(SubtaskAddForm, self).save()
        m.author = user
        m.save()
        m.subscribers.add(user)
        m.parent = parent
        m.save()
        return m

    # region Form fields settings

    subscribers = forms.MultipleChoiceField(
    widget=HiddenInput(),
        required=False
    )

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

    # endregion


class TaskEditForm(forms.ModelForm):
    """Class describing form of editing tasks"""

    class Meta:
        model = Task
        exclude = ["subscribers"]

    def save(self, user):
        """Overriding save-form method to set current id"""
        m = super(TaskEditForm, self).save()
        m.author = user
        m.save()
        m.subscribers.add(user)
        m.save()
        return m

    # region Form fields settings

    status = forms.ChoiceField(choices=Task.STATUS, widget=HiddenInput(), required=False)

    author = forms.ModelChoiceField(queryset=User.objects.all(), widget=HiddenInput(), required=False)

    description = forms.CharField(label='Info', required=False)

    start_date = forms.DateField(widget=DateInput(attrs={'class': 'datetime-input'}), label='Start', required=False)
    end_date = forms.DateField(widget=DateInput(attrs={'class': 'datetime-input'}), label='End')

    # endregion












