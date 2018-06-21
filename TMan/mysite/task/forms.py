from django import forms
from .models import *

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        exclude=[""]