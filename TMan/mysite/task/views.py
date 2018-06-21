from django.shortcuts import render
from .forms import TaskForm
from .models import Task

def home(request):
    form = TaskForm(request.POST or None)
    tasks = Task.objects.all()
    if request.method == "POST" and form.is_valid():
        print(request.POST)
        print(form.cleaned_data)

        data = form.cleaned_data
        print(form.cleaned_data['title'])
        print(data['title'])

        new_form = form.save()

    return render(request, 'task/home.html', locals())
