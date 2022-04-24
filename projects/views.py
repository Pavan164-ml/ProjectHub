from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import ProjectForm
# Create your views here.

def  projects(request):
    projects = Project.objects.all()
    return render(request, 'projects/projects.html', {"projects": projects})

def  project(request,pk):
    projectObj= Project.objects.get(id=pk)
    return render(request, 'projects/single-project.html', {"project": projectObj})

def  index(request):
    return render(request, 'main.html')

def createProject(request):
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('projects') 
    context = {"form": form}
    return render(request, 'projects/project_forms.html',context)

def updateProject(request,pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    # while rendering form we have to have data , 
    if request.method == 'POST':
        form = ProjectForm(request.POST,instance = project)
        if form.is_valid():
            form.save()
            
            return redirect('projects') 
    context = {"form": form}
    return render(request, 'projects/project_forms.html',context)



def deleteProject(request,pk):
    project = Project.objects.get(id=pk) 
    if request.method == 'POST':
       project.delete() 
       return redirect('projects') 
    context = {"project": project}
    return render(request, 'projects/delete_template.html',context) 
    