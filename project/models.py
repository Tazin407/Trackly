from django.db import models
from django.contrib.auth.models import User

class ProjectManager(models.Manager):
    def by_owner(self, user):
        return self.filter(owner=user)

class Project(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = ProjectManager()
    
    class Meta:
        unique_together = ['title', 'owner']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.owner.username}"