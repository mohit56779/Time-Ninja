from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# Import models
from django.contrib.auth.models import User
from .models import Project, Task, Entry

# View

@login_required
def projects(request):
    projects = Project.objects.filter(created_by=request.user)
    
    if request.method == 'POST':
        title = request.POST.get('title')

        if title:
            project = Project.objects.create( title=title, created_by=request.user)
            messages.info(request, 'The project was added!')

            return redirect('project:projects')

    return render(request, 'project/projects.html', {'projects' : projects})

@login_required
def project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == 'POST':
        title = request.POST.get('title')

        if title:
            task = Task.objects.create(project=project, created_by=request.user, title=title)

            messages.info(request, 'The task was added!')

            return redirect('project:project', project_id=project.id)

    tasks_todo = project.tasks.filter(status=Task.TODO)
    tasks_done = project.tasks.filter(status=Task.DONE)

    return render(request, 'project/project.html', {'project': project, 'tasks_todo': tasks_todo, 'tasks_done': tasks_done})



@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project,pk=project_id)

    if request.method == 'POST':
        title = request.POST.get('title')

        if title:
            project.title = title
            project.save()

            messages.info(request, 'The changes were saved!')

            return redirect('project:project', project_id=project.id)

    return render(request, 'project/edit_project.html', {'project': project})

@login_required
def task(request, project_id, task_id):
    project = get_object_or_404(Project, pk=project_id)
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        hours = int(request.POST.get('hours', 0))
        minutes = int(request.POST.get('minutes', 0))
        date = '%s %s' % (request.POST.get('date'), datetime.now().time())
        minutes_total = (hours * 60) + minutes
        note = request.POST.get('note', "")

        entry = Entry.objects.create(project=project, task=task, minutes=minutes_total, created_by=request.user, created_at=date,note=note, is_tracked=True)

    return render(request, 'project/task.html', {'today': datetime.today(), 'project': project, 'task': task})

@login_required
def edit_task(request, project_id, task_id):
    project = get_object_or_404(Project, pk=project_id)
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        status = request.POST.get('status')
        if title:
            task.title = title
            task.status = status
            task.save()

            messages.info(request, 'The changes were saved!')

            return redirect('project:task', project_id=project.id, task_id=task.id)

    return render(request, 'project/edit_task.html', {'project': project, 'task': task}) 

@login_required
def edit_entry(request, project_id, task_id, entry_id):
    project = get_object_or_404(Project, pk=project_id)
    task = get_object_or_404(Task, pk=task_id)
    entry = get_object_or_404(Entry, pk=entry_id)

    if request.method == 'POST':
        hours = int(request.POST.get('hours', 0))
        minutes = int(request.POST.get('minutes', 0))

        date = '%s %s' % (request.POST.get('date'), datetime.now().time())

        entry.created_at = date
        entry.minutes = (hours * 60) + minutes
        entry.save()

        messages.info(request, 'The changes was saved!')

        return redirect('project:task', project_id=project.id, task_id=task.id)

    hours, minutes = divmod(entry.minutes, 60)

    context = {
        'project': project,
        'task': task,
        'entry': entry,
        'hours': hours,
        'minutes': minutes
    }

    return render(request, 'project/edit_entry.html', context)

@login_required
def delete_entry(request, project_id, task_id, entry_id):
    project = get_object_or_404(Project, pk=project_id)
    task = get_object_or_404(Task, pk=task_id)
    entry = get_object_or_404(Entry, pk=entry_id)
    entry.delete()

    messages.info(request, 'The entry was deleted!')

    return redirect('project:task', project_id=project.id, task_id=task.id) 