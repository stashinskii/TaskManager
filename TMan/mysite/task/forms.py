from django import forms
from .models import *


from django.forms import ModelForm, HiddenInput, ModelChoiceField, DateInput


class SchedulerForm(forms.ModelForm):


    class Meta:
        model = SchedulerModel
        exclude = [""]
        widgets = {'start_date': DateInput(attrs={'type': 'date'}), 'end_date': DateInput(attrs={'type': 'date'}), }

    def save(self, user):
        """Overriding save-form method to set current id"""
        m = super(SchedulerForm, self).save()
        m.author = user
        m.save()
        return m

    title = forms.CharField(widget=forms.TextInput(attrs={'size':20, 'maxlength':30, 'placeholder':'Input title'} ))
    description = forms.CharField(label='Info', widget=forms.TextInput(attrs={'size': 20, 'maxlength': 200, 'placeholder': 'Input description'}))
    tag = forms.CharField(label='Info', widget=forms.TextInput(attrs={'size': 20, 'maxlength': 200, 'placeholder': 'Input tag'}))


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



class TaskForm(forms.ModelForm):
    """Class describing form of Task's adding"""

    class Meta:
        model = Task
        exclude = [""]
        widgets = {'start_date': DateInput(attrs={'type': 'date'}),
                   'end_date': DateInput(attrs={'type': 'date'}),
                }



    def save(self, user):
        """Overriding save-form method to set current id"""
        m = super(TaskForm, self).save()
        m.author = user
        m.save()
        m.subscribers.add(user)
        m.save()
        return m

    # region Form fields settings
    title = forms.CharField(widget=forms.TextInput(attrs={'size':20, 'maxlength':30, 'placeholder':'Input title'} ))
    description = forms.CharField(label='Info', widget=forms.TextInput(attrs={'size': 20, 'maxlength': 200, 'placeholder': 'Input description'}))
    tag = forms.CharField(label='Info', widget=forms.TextInput(attrs={'size': 20, 'maxlength': 200, 'placeholder': 'Input tag'}))
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
        widgets = {'start_date': DateInput(attrs={'type': 'date'}), 'end_date': DateInput(attrs={'type': 'date'}), }

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
        widgets = {'start_date': DateInput(attrs={'type': 'date'}), 'end_date': DateInput(attrs={'type': 'date'}), }

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

    title = forms.CharField(widget=forms.TextInput(attrs={'size':20, 'maxlength':30, 'placeholder':'Input title'} ))
    description = forms.CharField(label='Info', widget=forms.TextInput(attrs={'size': 20, 'maxlength': 200, 'placeholder': 'Input description'}))
    tag = forms.CharField(label='Info', widget=forms.TextInput(attrs={'size': 20, 'maxlength': 200, 'placeholder': 'Input tag'}))


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




    # endregion


class TaskEditForm(forms.ModelForm):
    """Class describing form of editing tasks"""

    class Meta:
        model = Task
        exclude = ["subscribers"]
        widgets = {'start_date': DateInput(attrs={'type': 'date'}), 'end_date': DateInput(attrs={'type': 'date'}), }


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


    # endregion












