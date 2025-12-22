from .models import Project

class ProjectService:
    @staticmethod
    def create_project(user, **data):
        data['owner'] = user
        return Project.objects.create(**data)
    
    @staticmethod
    def get_user_projects(user):
        return Project.objects.by_owner(user)
    
    @staticmethod
    def update_project_status(project_id, status):
        project = Project.objects.get(id=project_id)
        project.status = status
        project.save()
        return project