from django.shortcuts import render
from .models import Project, Skill

def home(request):
    projects = Project.objects.all().order_by('-created_at')
    featured_project = Project.objects.filter(is_featured=True).first()
    skills = Skill.objects.all().order_by('-proficiency')
    return render(request, 'portfolio/home.html', {
        'projects': projects, 
        'skills': skills,
        'featured_project': featured_project
    })
