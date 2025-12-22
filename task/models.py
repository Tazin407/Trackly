from django.db import models

class TaskManager(models.Manager):
    def by_status(self, status):
        return self.filter(status=status)
    
    def by_priority(self, priority):
        return self.filter(priority=priority)
    
    def by_project(self, project):
        return self.filter(project=project)
    
    def overdue(self):
        from django.utils import timezone
        return self.filter(due_date__lt=timezone.now().date(), status__in=['todo', 'in_progress'])

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    project = models.ForeignKey('project.Project', related_name='tasks', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = TaskManager()
    
    class Meta:
        ordering = ['-priority', '-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.project.name}"