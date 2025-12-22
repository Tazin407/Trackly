from .models import Task

class TaskService:
    @staticmethod
    def create_task(**data):
        return Task.objects.create(**data)
    
    @staticmethod
    def get_project_tasks(project):
        return Task.objects.by_project(project)
    
    @staticmethod
    def get_overdue_tasks():
        return Task.objects.overdue()
    
    @staticmethod
    def update_task_status(task_id, status):
        task = Task.objects.get(id=task_id)
        task.status = status
        task.save()
        return task
    
    @staticmethod
    def get_tasks_by_priority(priority):
        return Task.objects.by_priority(priority)