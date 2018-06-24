from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import TaskForm, TaskEditForm, SchedulerForm, TaskShareForm, SubtaskAddForm
from .models import Task
from .storage import get_user_tasks, order_by_status, get_subtasks, get_schedulers
from task_manager_library.models.task_model import Status
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



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

def global_search(request, string):
    current_user = request.user
    tasks = get_user_tasks(request.user)



    return render(request, 'task/global_search.html', locals())



def add_scheduler(request):
    current_user = request.user
    form = SchedulerForm(request.POST or None, initial={"status": 0, "last_added": timezone.now() })
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        new_form = form.save(request.user)
        #return redirect('') to list

    return render(request, 'task/add_scheduler.html', locals())


def get_scheduler_list(request):
    current_user = request.user
    schedulers = get_schedulers(current_user)
    return render(request, 'task/schedulers.html', locals())


@login_required(redirect_field_name='', login_url='/task/login')
def post_edit(request, id):
    current_user = request.user
    task = get_object_or_404(Task, pk=id)
    if request.method == "POST":
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(request.user)
            # TODO OVERRIDE AS IN SAVE METHOD
            #post.author = request.user

            task.save()
            return redirect('view', id=task.id)
    else:
        form = TaskEditForm(instance=task)
    return render(request, 'task/edit.html', locals())


def share_task(request, id):
    task = get_object_or_404(Task, pk=id)
    if request.method == "POST":
        form = TaskShareForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(request.user)
            task.save()
            return redirect('view', id=task.id)
    else:
        form = TaskShareForm(instance=task)
    return render(request, 'task/share.html', {'form': form})


def add_subtask(request, id):
    current_user = request.user
    parent_task = Task.objects.get(id=id)
    form = SubtaskAddForm(request.POST or None, initial={"status": 0})
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        new_form = form.save(request.user, parent_task)
        return redirect('view', id=id)

    return render(request, 'task/add.html', locals())



@login_required(redirect_field_name='', login_url='/task/login')
def add(request):
    current_user = request.user
    form = TaskForm(request.POST or None, initial={"status": 0})
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        new_form = form.save(request.user)
        return redirect('/task/home')

    return render(request, 'task/add.html', locals())



@login_required(redirect_field_name='', login_url='/task/login')
def home(request, status=None):
    """
    Home page of Task manager
    If you are not logged in - you will be redirect to login page
    After login you will be automatically redirect to this page
    """
    current_user = request.user

    tasks = get_user_tasks(request.user)

    query = request.GET.get("q")
    if query:
        tasks = Task.objects.filter(subscribers=current_user, parent=None, title__icontains=query)

    if status is not None:
        tasks = Task.objects.filter(subscribers=current_user, parent=None, status=2)

    paginator = Paginator(tasks, 3)

    page = request.GET.get('page')



    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tasks = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tasks = paginator.page(paginator.num_pages)

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










