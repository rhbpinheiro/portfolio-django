# Guia de Configuração do Projeto Django Portfolio

Este guia descreve o passo a passo para configurar o ambiente e iniciar o projeto Django no Windows.

## 1. Criar o Ambiente Virtual
Crie um ambiente virtual para isolar as dependências do projeto.

```powershell
python -m venv .venv
```

## 2. Ativar o Ambiente Virtual
Ative o ambiente virtual antes de instalar qualquer pacote.

```powershell
.venv\Scripts\activate
```

## 3. Instalar o Django
Com o ambiente virtual ativo, instale a versão mais recente do Django.

```powershell
pip install django
```

## 4. Criar o Projeto Django
Inicie o projeto `portfolio_project` no diretório atual (o ponto `.` indica o diretório atual).

```powershell
django-admin startproject portfolio_project .
```

## 5. Criar o App Portfolio
Crie o aplicativo `portfolio` onde ficará a lógica do portfolio.

```powershell
python manage.py startapp portfolio
```

## 6. Configurar settings.py

Agora vamos configurar o arquivo `portfolio_project/settings.py` para reconhecer nosso app e gerenciar arquivos estáticos/mídia.

### 6.1. Registrar o App
Procure pela lista `INSTALLED_APPS` e adicione `'portfolio',` ao final ou no início da lista de apps locais.

```python
INSTALLED_APPS = [
    # ... apps do django ...
    'portfolio',
]
```

### 6.2. Configurar Templates
Localize a configuração `TEMPLATES`. Em `DIRS`, adicione o caminho para uma pasta de templates na raiz (opcional, mas recomendado) ou garanta que `APP_DIRS` esteja `True`.

```python
TEMPLATES = [
    {
        # ...
        'DIRS': [], # Se criar uma pasta templates na raiz, coloque [BASE_DIR / 'templates']
        'APP_DIRS': True,
        # ...
    },
]
```

### 6.3. Arquivos Estáticos e Mídia
Como você optou por organizar os arquivos dentro do app `portfolio`, a estrutura de pastas será:

- **Templates:** `portfolio/templates/portfolio/`
- **Static:** `portfolio/static/portfolio/`
- **Media:** `media/` (Na raiz do projeto, pois são uploads)

No `settings.py`, adicione/configure no final do arquivo:

```python
import os

STATIC_URL = 'static/'
# Não é necessário STATICFILES_DIRS se usar apenas pastas dentro dos apps

# Configuração de Media (Uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

> **Importante:** Lembre-se de adicionar `'portfolio'` em `INSTALLED_APPS` para que o Django encontre essas pastas automaticamente.

## 7. Criar Modelos (Models)
Agora vamos definir a estrutura do banco de dados no arquivo `portfolio/models.py`.

### 7.1. Definir Models
Substitua o conteúdo de `portfolio/models.py` pelo seguinte código:

```python
from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')
    link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Skill(models.Model):
    name = models.CharField(max_length=50)
    proficiency = models.IntegerField(help_text="0 to 100")
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon class")

    def __str__(self):
        return self.name
```

### 7.2. Criar e Aplicar Migrations
Sempre que modificamos o `models.py`, precisamos atualizar o banco de dados.

```powershell
python manage.py makemigrations
python manage.py migrate
```

## 8. Criar App de Gerenciamento (`manager`)

Excelente ideia! Vamos criar um app separado chamado `manager` para controlar a área administrativa. Isso treina a comunicação entre apps (importar models de um app em outro).

### 8.1. Criar o App Manager
Rode o comando no terminal:

```powershell
python manage.py startapp manager
```

### 8.2. Registrar o App `manager`
Vá em `portfolio_project/settings.py` e adicione `'manager'` na lista `INSTALLED_APPS`.

```python
INSTALLED_APPS = [
    # ...
    'portfolio',
    'manager',
]
```

### 8.3. Criar Formulários no Manager (`manager/forms.py`)
Crie o arquivo `manager/forms.py`. Note que precisamos importar os models do **outro app** (`portfolio`).

```python
from django import forms
from portfolio.models import Project, Skill

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'image', 'link']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título do Projeto'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição', 'rows': 3}),
            'link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'URL do Projeto'}),
        }

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'proficiency', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Skill (Ex: Python)'}),
            'proficiency': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Classe do Ícone (Ex: fa-brands fa-python)'}),
        }
```

### 8.4. Criar Views do Manager (Class-Based Views)
No arquivo `manager/views.py`, vamos usar as Views Genéricas do Django (CBVs) para um código mais limpo e moderno.

```python
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from portfolio.models import Project, Skill
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
```

### 8.5. Configurar URLs do Manager (`manager/urls.py`)
Atualize o arquivo `manager/urls.py` para usar as classes (`.as_view()`):

```python
from django.urls import path
from .views import DashboardView, ProjectCreateView, ProjectUpdateView, ProjectDeleteView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('project/new/', ProjectCreateView.as_view(), name='project_create'),
    path('project/<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_update'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
]
```

### 8.6. Incluir URLs no Projeto Principal (`portfolio_project/urls.py`)
(Se você já fez este passo, pode pular)

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portfolio.urls')),
    path('manager/', include('manager.urls')),
]
## 9. Templates e Design (Azul Neon com Tailwind CSS)

Podemos usar **Tailwind CSS**! É uma escolha excelente e moderna. Para simplificar e não precisar instalar Node.js/NPM agora, vamos usar via CDN com a configuração do tema Neon diretamente no HTML.

### 9.1. Estrutura de Pastas
Dentro do app `manager`, crie as pastas (se ainda não criou):
`manager/templates/manager/`

### 9.2. Template Base (`base.html`)
Crie ou edite `manager/templates/manager/base.html`.
Adicionamos o script do Tailwind e configuramos as cores `neon-blue` e `neon-secondary` nele.

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Manager{% endblock %} | Portfolio</title>
    <!-- Tailwind CSS (via CDN para dev) -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        bg: '#0a0a0a',
                        card: '#161616',
                        'neon-blue': '#00f3ff',     /* Azul Neon Principal */
                        'neon-secondary': '#0088ff', /* Azul Secundário */
                    },
                    boxShadow: {
                        'neon': '0 0 10px #00f3ff',
                        'neon-hover': '0 0 20px #00f3ff, 0 0 40px #00f3ff',
                    }
                }
            }
        }
    </script>
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background-color: #0a0a0a; color: #e0e0e0; }
        /* Inputs do Django Form */
        input[type="text"], input[type="number"], input[type="url"], input[type="file"], textarea, select {
            background-color: #222;
            border: 1px solid #444;
            color: white;
            padding: 0.5rem;
            border-radius: 0.375rem; 
            width: 100%;
        }
        input:focus, textarea:focus, select:focus {
            outline: none;
            border-color: #00f3ff;
            box-shadow: 0 0 10px rgba(0, 243, 255, 0.3);
        }
    </style>
</head>
<body class="bg-bg text-gray-200 font-sans min-h-screen flex flex-col">

    <!-- Navbar -->
    <nav class="bg-black/80 border-b-2 border-neon-blue shadow-neon mb-8">
        <div class="container mx-auto px-4 py-4 flex justify-between items-center">
            <a class="text-neon-blue font-bold text-xl tracking-wider uppercase drop-shadow-[0_0_5px_rgba(0,243,255,0.8)]" href="{% url 'dashboard' %}">
                <i class="fas fa-terminal mr-2"></i>Dev Manager
            </a>
            <div>
                <a href="{% url 'home' %}" class="px-4 py-2 border border-gray-600 rounded hover:border-neon-blue hover:text-neon-blue transition-all duration-300 text-sm">
                    Ver Site
                </a>
            </div>
        </div>
    </nav>

    <!-- Conteúdo Principal -->
    <div class="container mx-auto px-4 flex-grow">
        {% block content %}{% endblock %}
    </div>

    <!-- Footer Simples -->
    <footer class="text-center py-6 text-gray-600 text-sm mt-8">
        &copy; 2026 Portfolio Manager
    </footer>

</body>
</html>
```

### 9.3. Dashboard (`dashboard.html`)
Crie `manager/templates/manager/dashboard.html`.

```html
{% extends 'manager/base.html' %}

{% block title %}Dashboard{% endblock %}

{% block content %}
<div class="flex justify-between items-center mb-8">
    <h1 class="text-3xl font-bold text-neon-blue drop-shadow-[0_0_5px_rgba(0,243,255,0.5)]">Dashboard</h1>
    <a href="{% url 'project_create' %}" class="px-4 py-2 border border-neon-blue text-neon-blue rounded hover:bg-neon-blue hover:text-black hover:shadow-neon-hover transition-all duration-300 flex items-center shadow-neon">
        <i class="fas fa-plus mr-2"></i>Novo Projeto
    </a>
</div>

<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    {% for project in projects %}
    <div class="bg-card border border-gray-800 rounded-lg overflow-hidden hover:-translate-y-1 hover:border-neon-secondary hover:shadow-[0_5px_15px_rgba(0,136,255,0.2)] transition-all duration-300 flex flex-col h-full">
        {% if project.image %}
        <div class="h-48 overflow-hidden">
            <img src="{{ project.image.url }}" class="w-full h-full object-cover" alt="{{ project.title }}">
        </div>
        {% endif %}
        
        <div class="p-5 flex-grow">
            <h5 class="text-xl font-bold text-white mb-2">{{ project.title }}</h5>
            <p class="text-gray-400 text-sm mb-4 line-clamp-3">{{ project.description }}</p>
        </div>

        <div class="p-5 pt-0 mt-auto flex justify-between border-t border-gray-800/50 pt-4">
            <a href="{% url 'project_update' project.pk %}" class="text-sm text-cyan-400 hover:text-white transition-colors">
                <i class="fas fa-edit mr-1"></i>Editar
            </a>
            <a href="{% url 'project_delete' project.pk %}" class="text-sm text-red-500 hover:text-red-400 transition-colors">
                <i class="fas fa-trash-alt mr-1"></i>Excluir
            </a>
        </div>
    </div>
    {% empty %}
    <div class="col-span-full text-center py-12 text-gray-500">
        <p class="text-xl">Nenhum projeto cadastrado.</p>
        <p class="text-sm mt-2">Clique em "Novo Projeto" para começar.</p>
    </div>
    {% endfor %}
</div>
{% endblock %}
```

### 9.4. Formulário de Projeto (`project_form.html`)
Crie `manager/templates/manager/project_form.html`.

```html
{% extends 'manager/base.html' %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
<div class="max-w-2xl mx-auto">
    <div class="bg-card border border-gray-800 rounded-lg p-8 shadow-lg">
        <h3 class="text-2xl font-bold text-neon-blue mb-6 border-b border-gray-800 pb-2">{{ title }}</h3>
        
        <form method="post" enctype="multipart/form-data" class="space-y-6">
            {% csrf_token %}
            
            {% for field in form %}
            <div>
                <label class="block text-sm font-medium text-gray-300 mb-1">{{ field.label }}</label>
                {{ field }}
                {% if field.errors %}
                <div class="text-red-500 text-xs mt-1">{{ field.errors }}</div>
                {% endif %}
                {% if field.help_text %}
                <div class="text-gray-500 text-xs mt-1">{{ field.help_text }}</div>
                {% endif %}
            </div>
            {% endfor %}

            <div class="flex justify-end space-x-4 pt-4 border-t border-gray-800">
                <a href="{% url 'dashboard' %}" class="px-4 py-2 text-gray-400 hover:text-white transition-colors">Cancelar</a>
                <button type="submit" class="px-6 py-2 bg-transparent border border-neon-blue text-neon-blue rounded hover:bg-neon-blue hover:text-black hover:shadow-neon transition-all duration-300 font-bold">
                    Salvar Projeto
                </button>
            </div>
        </form>
    </div>
</div>
{% endblock %}
```

### 9.5. Confirmação de Exclusão (`project_confirm_delete.html`)
Crie `manager/templates/manager/project_confirm_delete.html`.

```html
{% extends 'manager/base.html' %}

{% block title %}Excluir Projeto{% endblock %}

{% block content %}
<div class="max-w-md mx-auto mt-20">
    <div class="bg-card border border-red-900/50 rounded-lg p-8 shadow-[0_0_15px_rgba(255,0,0,0.2)] text-center">
        <div class="text-red-500 text-5xl mb-6">
            <i class="fas fa-exclamation-triangle"></i>
        </div>
        
        <h3 class="text-2xl font-bold text-white mb-4">Tem certeza?</h3>
        <p class="text-gray-400 mb-8">
            Você está prestes a excluir o projeto <strong class="text-white">"{{ object.title }}"</strong>.<br>
            Esta ação não pode ser desfeita.
        </p>
        
        <form method="post">
            {% csrf_token %}
            <div class="flex justify-center space-x-4">
                <a href="{% url 'dashboard' %}" class="px-6 py-2 border border-gray-600 rounded text-gray-300 hover:bg-gray-800 transition-colors">
                    Cancelar
                </a>
                <button type="submit" class="px-6 py-2 bg-red-600/20 border border-red-600 text-red-500 rounded hover:bg-red-600 hover:text-white transition-all duration-300 font-bold shadow-[0_0_10px_rgba(220,38,38,0.3)]">
                    Sim, Excluir
                </button>
            </div>
        </form>
    </div>
</div>
{% endblock %}
## 10. Configurar Autenticação

Como protegemos as views com `@login_required` (ou `LoginRequiredMixin`), precisamos configurar o Login.

### 10.1. Configurar URLs de Auth
No arquivo `portfolio_project/urls.py`, vamos adicionar as URLs de autenticação do Django, mas apontando para o nosso template customizado.

```python
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views # Importante

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portfolio.urls')),
    path('manager/', include('manager.urls')),
    
    # Rota de Login Customizada
    path('accounts/login/', auth_views.LoginView.as_view(template_name='manager/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]
```

### 10.2. Configurar `settings.py`
No final do arquivo `settings.py`, adicione:

```python
# Redirecionamento após login (vai para o dashboard)
LOGIN_REDIRECT_URL = 'dashboard'
# Redirecionamento após logout
LOGOUT_REDIRECT_URL = 'home'
# URL de login (caso tente acessar página protegida sem logar)
LOGIN_URL = 'login'
```

### 10.3. Criar Template de Login (`login.html`)
Crie o arquivo `manager/templates/manager/login.html`.

```html
{% extends 'manager/base.html' %}

{% block title %}Login{% endblock %}

{% block content %}
<div class="min-h-[80vh] flex items-center justify-center">
    <div class="max-w-md w-full bg-card border border-gray-800 rounded-lg p-8 shadow-[0_0_20px_rgba(0,243,255,0.1)]">
        <h2 class="text-3xl font-bold text-center text-neon-blue mb-8 drop-shadow-[0_0_5px_rgba(0,243,255,0.8)]">
            <i class="fas fa-user-lock mr-2"></i>Acesso Restrito
        </h2>
        
        <form method="post" class="space-y-6">
            {% csrf_token %}
            
            {% if form.errors %}
            <div class="bg-red-900/30 border border-red-500 text-red-200 p-3 rounded text-sm text-center">
                Usuário ou senha incorretos.
            </div>
            {% endif %}

            <div>
                <label class="block text-gray-400 text-sm font-bold mb-2">Usuário</label>
                <input type="text" name="username" class="w-full bg-gray-900 border border-gray-700 rounded p-3 text-white focus:border-neon-blue focus:outline-none focus:shadow-[0_0_10px_rgba(0,243,255,0.3)] transition-all" autofocus required>
            </div>

            <div>
                <label class="block text-gray-400 text-sm font-bold mb-2">Senha</label>
                <input type="password" name="password" class="w-full bg-gray-900 border border-gray-700 rounded p-3 text-white focus:border-neon-blue focus:outline-none focus:shadow-[0_0_10px_rgba(0,243,255,0.3)] transition-all" required>
            </div>

            <button type="submit" class="w-full py-3 bg-transparent border border-neon-blue text-neon-blue rounded font-bold hover:bg-neon-blue hover:text-black hover:shadow-neon transition-all duration-300 uppercase tracking-wider">
                Entrar
            </button>
        </form>
    </div>
</div>
{% endblock %}
```

### 10.4. Criar Superusuário
Para acessar, você precisa de um usuário. Crie um no terminal:

```powershell
python manage.py createsuperuser
```
(Siga as instruções: nome, email (opcional), senha)


## 11. Interface Pública (Design do Currículo)

Finalmente, vamos criar a página inicial que os visitantes verão. Ela deve ser bonita, moderna e listar seus projetos e habilidades dinamicamente.

### 11.1. Estrutura de Pastas
Dentro do app `portfolio`, crie a estrutura de templates:
`portfolio/templates/portfolio/`

### 11.2. Layout Base Público (`base.html`)
Crie `portfolio/templates/portfolio/base.html`. Vamos usar o **Tailwind CSS** novamente para manter o padrão Neon.

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rodolpho Pinheiro | Desenvolvedor Python</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        bg: '#0a0a0a',
                        card: '#161616',
                        'neon-blue': '#00f3ff',
                        'neon-secondary': '#0088ff',
                    },
                    boxShadow: {
                        'neon': '0 0 10px #00f3ff',
                        'neon-hover': '0 0 20px #00f3ff, 0 0 40px #00f3ff',
                    }
                }
            }
        }
    </script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background-color: #0a0a0a; color: #e0e0e0; }
        .hero-pattern {
            background-color: #0a0a0a;
            background-image: radial-gradient(#00f3ff 1px, transparent 1px);
            background-size: 50px 50px;
            opacity: 0.1;
        }
    </style>
</head>
<body class="font-sans antialiased selection:bg-neon-blue selection:text-black">

    <!-- Navbar Transparente -->
    <nav class="fixed w-full z-50 bg-black/80 backdrop-blur-md border-b border-gray-800">
        <div class="container mx-auto px-6 py-4 flex justify-between items-center">
            <a href="#" class="text-2xl font-bold text-white tracking-tighter">
                RODOLPHO<span class="text-neon-blue">.DEV</span>
            </a>
            <div class="hidden md:flex space-x-8 text-sm font-medium">
                <a href="#about" class="hover:text-neon-blue transition-colors">Sobre</a>
                <a href="#skills" class="hover:text-neon-blue transition-colors">Skills</a>
                <a href="#projects" class="hover:text-neon-blue transition-colors">Projetos</a>
                <a href="#contact" class="hover:text-neon-blue transition-colors">Contato</a>
            </div>
            <a href="{% url 'login' %}" class="text-xs text-gray-500 hover:text-white transition-colors">
                <i class="fas fa-lock"></i>
            </a>
        </div>
    </nav>

    {% block content %}{% endblock %}

    <!-- Footer -->
    <footer class="bg-black py-8 border-t border-gray-800 text-center text-gray-500 text-sm">
        <p>&copy; 2026 Rodolpho Pinheiro. Built with <span class="text-neon-blue">Django & Tailwind</span>.</p>
    </footer>

</body>
</html>
```

### 11.3. Página Inicial (`home.html`)
Crie `portfolio/templates/portfolio/home.html`. Aqui exibiremos os projetos e skills cadastrados no banco.

```html
{% extends 'portfolio/base.html' %}

{% block content %}
<!-- Hero Section -->
<section class="relative min-h-screen flex items-center justify-center pt-20 overflow-hidden" id="about">
    <div class="absolute inset-0 hero-pattern"></div>
    <div class="container mx-auto px-6 relative z-10 text-center">
        <div class="inline-block mb-4 px-3 py-1 border border-neon-blue/30 rounded-full bg-neon-blue/10 text-neon-blue text-xs font-bold tracking-widest uppercase">
            Full Stack  Developer
        </div>
        <h1 class="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight">
            Transformando ideias em<br>
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-neon-blue to-neon-secondary drop-shadow-[0_0_10px_rgba(0,243,255,0.5)]">
                Código de Alto Nível
            </span>
        </h1>
        <p class="text-gray-400 text-lg md:text-xl max-w-2xl mx-auto mb-10">
            Especialista em Django e Automações. Crio soluções web robustas, escaláveis e com design impactante.
        </p>
        <div class="flex justify-center gap-4">
            <a href="#projects" class="px-8 py-3 bg-neon-blue text-black font-bold rounded hover:shadow-neon hover:scale-105 transition-all duration-300">
                Ver Projetos
            </a>
            <a href="https://github.com/rhbpinheiro" target="_blank" class="px-8 py-3 border border-gray-700 rounded text-white hover:border-neon-blue hover:text-neon-blue transition-all duration-300">
                <i class="fab fa-github mr-2"></i>GitHub
            </a>
        </div>
    </div>
</section>

<!-- Skills Section -->
<section class="py-20 bg-card/50" id="skills">
    <div class="container mx-auto px-6">
        <h2 class="text-3xl font-bold text-white mb-12 text-center">Tech Stack</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-6">
            {% for skill in skills %}
            <div class="bg-black border border-gray-800 p-6 rounded-lg text-center hover:border-neon-blue hover:shadow-neon transition-all duration-300 group">
                <div class="text-4xl text-gray-500 group-hover:text-neon-blue mb-4 transition-colors">
                    {% if skill.icon %}
                        <i class="{{ skill.icon }}"></i>
                    {% else %}
                        <i class="fas fa-code"></i>
                    {% endif %}
                </div>
                <h3 class="text-white font-bold">{{ skill.name }}</h3>
                <div class="w-full bg-gray-800 h-1 mt-4 rounded-full overflow-hidden">
                    <div class="bg-neon-blue h-full" style="width: {{ skill.proficiency }}%"></div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</section>

<!-- Projects Section -->
<section class="py-20" id="projects">
    <div class="container mx-auto px-6">
        <h2 class="text-3xl font-bold text-white mb-12 text-center">Projetos Recentes</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {% for project in projects %}
            <div class="bg-card border border-gray-800 rounded-xl overflow-hidden hover:-translate-y-2 hover:shadow-[0_10px_30px_rgba(0,243,255,0.15)] transition-all duration-500 group">
                {% if project.image %}
                <div class="h-48 overflow-hidden relative">
                    <img src="{{ project.image.url }}" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700" alt="{{ project.title }}">
                    <div class="absolute inset-0 bg-gradient-to-t from-card to-transparent opacity-80"></div>
                </div>
                {% endif %}
                <div class="p-6 relative">
                    <h3 class="text-2xl font-bold text-white mb-3 group-hover:text-neon-blue transition-colors">{{ project.title }}</h3>
                    <p class="text-gray-400 mb-6 text-sm leading-relaxed line-clamp-3">
                        {{ project.description }}
                    </p>
                    {% if project.link %}
                    <a href="{{ project.link }}" target="_blank" class="inline-flex items-center text-neon-blue text-sm font-bold uppercase tracking-wider hover:underline">
                        Acessar Projeto <i class="fas fa-arrow-right ml-2"></i>
                    </a>
                    {% endif %}
                </div>
            </div>
            {% empty %}
            <p class="text-gray-500 text-center col-span-full">Em breve novos projetos.</p>
            {% endfor %}
        </div>
    </div>
</section>
{% endblock %}
```





