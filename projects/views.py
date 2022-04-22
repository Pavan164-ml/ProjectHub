from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def  projects(request):
    return render(request, 'projects/projects.html')

def  project(request):
    projectone = "This is pavan's project"
    return render(request, 'projects/project.html', {"p1": projectone})

def  index(request):
    return render(request, 'main.html')