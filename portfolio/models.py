from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')
    link = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False, verbose_name="Destaque")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Skill(models.Model):
    name = models.CharField(max_length=50)
    proficiency = models.IntegerField(help_text="0 to 100")
    icon = models.CharField(max_length=50, blank=True, help_text="Ex: 'fab fa-python', 'fab fa-js', 'fas fa-database'")
    image = models.ImageField(upload_to='skills/', blank=True, null=True, verbose_name="Ícone Personalizado (Imagem)")

    def __str__(self):
        return self.name
