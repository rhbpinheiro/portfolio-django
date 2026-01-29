from django.db import models
from portfolio.models import Project, Skill


class ProjectManager(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    manager = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.project} - {self.manager}"

        




