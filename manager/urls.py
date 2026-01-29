from django.urls import path
from django.urls import path
from .views import DashboardView, ProjectCreateView, ProjectUpdateView, ProjectDeleteView, SkillCreateView, SkillUpdateView, SkillDeleteView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    
    # Projects
    path('project/new/', ProjectCreateView.as_view(), name='project_create'),
    path('project/<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_update'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),

    # Skills
    path('skill/new/', SkillCreateView.as_view(), name='skill_create'),
    path('skill/<int:pk>/edit/', SkillUpdateView.as_view(), name='skill_update'),
    path('skill/<int:pk>/delete/', SkillDeleteView.as_view(), name='skill_delete'),
]