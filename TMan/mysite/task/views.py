from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import TaskForm, TaskEditForm
from .models import Task
from .storage import get_user_tasks, order_by_status, get_subtasks
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
def view(request, id):
    task = Task.objects.get(id=id)
    subtasks = get_subtasks(request.user, task)
    current_user = request.user
    return render(request, 'task/view.html', locals())


@login_required(redirect_field_name='', login_url='/task/login')
def post_edit(request, id):
    task = get_object_or_404(Task, pk=id)
    if request.method == "POST":

        # TODO ADD EditForm

        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(request.user)
            # TODO OVERRIDE AS IN SAVE METHOD
            #post.author = request.user

            task.save()
            return redirect('view', id=task.id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'task/edit.html', {'form': form})


@login_required(redirect_field_name='', login_url='/task/login')
def add(request):
    current_user = request.user
    form = TaskForm(request.POST or None, initial={"status": 0})
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        new_form = form.save(request.user)

    return render(request, 'task/add.html', locals())



@login_required(redirect_field_name='', login_url='/task/login')
def home(request):
    """
    Home page of Task manager
    If you are not logged in - you will be redirect to login page
    After login you will be automatically redirect to this page
    """
    current_user = request.user

    tasks = get_user_tasks(request.user)

    return render(request, 'task/home.html', locals())


def tag_search(request, tag):
    current_user = request.user
    tasks = Task.objects.filter(tag=tag)
    return render(request, 'task/search.html', locals())


def delete(request, id):
    person = Task.objects.get(id=id)
    person.delete()
    return redirect('/task/home')


def done(request, id):
    person = Task.objects.get(id=id)
    person.status=2
    person.save()
    return redirect('view', id=id)



def begin(request, id):
    person = Task.objects.get(id=id)
    person.status = 1
    person.save()
    return redirect('view', id=id)










