from django import forms
from portfolio.models import Project, Skill

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'image', 'link', 'is_featured']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título do Projeto'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição do Projeto', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Link do Projeto'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-checkbox h-5 w-5 text-neon-blue rounded focus:ring-neon-secondary'}),
        }

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'proficiency', 'icon', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Habilidade'}),
            'proficiency': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Nível de Proficiência', 'min': '0', 'max': '100'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ícone da Habilidade (Ex: fa-brands fa-python)'}),
            'image': forms.FileInput(attrs={'class': 'w-full'}),
        }