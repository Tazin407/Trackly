from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from project.models import Project
from task.models import Task

class TaskProjectOwnershipTest(TestCase):
    def test_task_must_belong_to_owned_project(self):
        # Setup
        owner = User.objects.create_user(username='owner', password='password')
        other_user = User.objects.create_user(username='other', password='password')
        
        owned_project = Project.objects.create(title='Owned Project', owner=owner)
        unowned_project = Project.objects.create(title='Unowned Project', owner=other_user)
        
        client = APIClient()
        client.force_authenticate(user=owner)
        
        response = client.post('/api/tasks/', {
            'title': 'New Task',
            'description': 'Task for owned project',
            'project': unowned_project.id  # Attempt to assign task to unowned project
        })
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
