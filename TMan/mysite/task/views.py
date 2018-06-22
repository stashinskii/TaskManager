from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import TaskForm, TaskEditForm
from .models import Task
from .storage import get_user_tasks, order_by_status
from task_manager_library.models.task_model import Status


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
def edit_task(request):
    #TODO GET ID
    form = TaskEditForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        new_form = form.update(50)

    return render(request, 'task/home.html', locals())


def delete(request, id):
    person = Task.objects.get(id=id)
    person.delete()
    return redirect('/task/home')


def done(request, id):
    person = Task.objects.get(id=id)
    person.status=3
    person.save()
    return redirect('/task/home')


def undone(request, id):
    person = Task.objects.get(id=id)
    person.status = 0
    person.save()
    return redirect('/task/home')


def begin(request, id):
    person = Task.objects.get(id=id)
    person.status = 2
    person.save()
    return redirect('/task/home')


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


def home_done(request):
    current_user = request.user
    form = TaskForm(request.POST or None, initial={"status": 0})
    tasks = order_by_status(request.user, 3)
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        new_form = form.save(request.user)

    return render(request, 'task/home.html', locals())


def home_undone(request):
    current_user = request.user
    form = TaskForm(request.POST or None, initial={"status": 0})
    tasks = order_by_status(request.user, 0)
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        new_form = form.save(request.user)

    return render(request, 'task/home.html', locals())


def home_process(request):
    current_user = request.user
    form = TaskForm(request.POST or None, initial={"status": 0})
    tasks = order_by_status(request.user, 2)
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        new_form = form.save(request.user)

    return render(request, 'task/home.html', locals())









