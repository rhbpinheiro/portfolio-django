from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from portfolio.models import Project, Skill # Importação Cross-App
from .forms import ProjectForm, SkillForm


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'manager/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        context['skills'] = Skill.objects.all()
        return context

# --- PROJETOS ---
class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'manager/project_form.html'
    success_url = reverse_lazy('dashboard')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Novo Projeto'
        return context

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'manager/project_form.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Projeto'
        return context

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'manager/project_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

# --- SKILLS ---
class SkillCreateView(LoginRequiredMixin, CreateView):
    model = Skill
    form_class = SkillForm
    template_name = 'manager/skill_form.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nova Habilidade'
        return context

class SkillUpdateView(LoginRequiredMixin, UpdateView):
    model = Skill
    form_class = SkillForm
    template_name = 'manager/skill_form.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Habilidade'
        return context

class SkillDeleteView(LoginRequiredMixin, DeleteView):
    model = Skill
    template_name = 'manager/skill_confirm_delete.html'
    success_url = reverse_lazy('dashboard')