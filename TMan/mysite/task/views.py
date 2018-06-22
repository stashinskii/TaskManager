from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from .models import Task
from .storage import get_user_tasks


def register(request):
    """
    Registration view
    Recieve request and return rendered page or redirects you to homepage
    """
    if request.method == "POST":
        creation_form = UserCreationForm(request.POST)
        if creation_form.is_valid():
            creation_form.save()
            return redirect('/task/home')
    else:
        creation_form = UserCreationForm()

        args = {'form': creation_form}

        return render(request, 'registration/register.html', args)


@login_required(redirect_field_name='', login_url='/task/login')
def home(request):
    """
    Home page of Task manager
    If you are not logged in - you will be redirect to login page
    After login you will be automatically redirect to this page
    """
    current_user = request.user
    form = TaskForm(request.POST or None, initial={"status": 0})
    tasks = get_user_tasks(request.user)
    if request.method == "POST" and form.is_valid():

        data = form.cleaned_data
        new_form = form.save(request.user)

    return render(request, 'task/home.html', locals())




