from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from rest_framework.validators import ValidationError
from django.shortcuts import get_object_or_404
from .models import Task
from .serializers import TaskSerializer, TaskCreateSerializer
from .services import TaskService
from project.models import Project


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing tasks within projects.
    Provides CRUD operations with proper authorization and filtering.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return tasks for projects owned by the authenticated user."""
        queryset = Task.objects.filter(project__owner=self.request.user)
        
        # Filter by project if specified
        project_id = self.request.query_params.get('project')
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        
        # Filter by status if specified
        task_status = self.request.query_params.get('status')
        if task_status:
            queryset = queryset.filter(status=task_status)
        
        # Filter by priority if specified
        priority = self.request.query_params.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        return queryset
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return TaskCreateSerializer
        return TaskSerializer
    
    def list(self, request, *args, **kwargs):
        """List tasks with optional filtering."""
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            
            return Response(
                {
                    'success': True,
                    'message': 'Tasks retrieved successfully',
                    'data': serializer.data,
                    'count': queryset.count()
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'success': False,
                    'message': 'Failed to retrieve tasks',
                    'errors': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Create a new task."""
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Verify project ownership
            project = serializer.validated_data['project']
            if project.owner != request.user:
                return Response(
                    {
                        'success': False,
                        'message': 'You are not authorized to create tasks in this project'
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            
            task = TaskService.create_task(**serializer.validated_data)
            response_serializer = TaskSerializer(task)
            
            return Response(
                {
                    'success': True,
                    'message': 'Task created successfully',
                    'data': response_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return Response(
                {
                    'success': False,
                    'message': 'Validation error',
                    'errors': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'success': False,
                    'message': 'Failed to create task',
                    'errors': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific task."""
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            
            return Response(
                {
                    'success': True,
                    'message': 'Task retrieved successfully',
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Task.DoesNotExist:
            return Response(
                {
                    'success': False,
                    'message': 'Task not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """Update a task."""
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response(
                {
                    'success': True,
                    'message': 'Task updated successfully',
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response(
                {
                    'success': False,
                    'message': 'Validation error',
                    'errors': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'success': False,
                    'message': 'Failed to update task',
                    'errors': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def destroy(self, request, *args, **kwargs):
        """Delete a task."""
        try:
            instance = self.get_object()
            instance.delete()
            
            return Response(
                {
                    'success': True,
                    'message': 'Task deleted successfully'
                },
                status=status.HTTP_204_NO_CONTENT
            )
        except Task.DoesNotExist:
            return Response(
                {
                    'success': False,
                    'message': 'Task not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Update task status."""
        try:
            task = self.get_object()
            new_status = request.data.get('status')
            
            if not new_status:
                return Response(
                    {
                        'success': False,
                        'message': 'Status is required'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validate status choice
            valid_statuses = [choice[0] for choice in Task.STATUS_CHOICES]
            if new_status not in valid_statuses:
                return Response(
                    {
                        'success': False,
                        'message': f'Invalid status. Valid choices are: {", ".join(valid_statuses)}'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            task.status = new_status
            task.save()
            
            serializer = self.get_serializer(task)
            return Response(
                {
                    'success': True,
                    'message': 'Task status updated successfully',
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'success': False,
                    'message': 'Failed to update task status',
                    'errors': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get overdue tasks for the authenticated user."""
        try:
            overdue_tasks = Task.objects.overdue().filter(project__owner=request.user)
            serializer = self.get_serializer(overdue_tasks, many=True)
            
            return Response(
                {
                    'success': True,
                    'message': 'Overdue tasks retrieved successfully',
                    'data': serializer.data,
                    'count': overdue_tasks.count()
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'success': False,
                    'message': 'Failed to retrieve overdue tasks',
                    'errors': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )