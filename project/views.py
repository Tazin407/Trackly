from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Project
from .serializers import ProjectSerializer, ProjectCreateSerializer
from .services import ProjectService


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user projects.
    Provides CRUD operations for projects with proper authorization.
    """
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return projects owned by the authenticated user."""
        return ProjectService.get_user_projects(self.request.user)
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return ProjectCreateSerializer
        return ProjectSerializer
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Create a new project for the authenticated user."""
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            project = ProjectService.create_project(
                request.user, **serializer.validated_data
            )
            
            response_serializer = ProjectSerializer(project)
            return Response(
                {
                    'success': True,
                    'message': 'Project created successfully',
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
                    'message': 'An error occurred while creating the project',
                    'errors': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def list(self, request, *args, **kwargs):
        """List all projects for the authenticated user."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        return Response(
            {
                'success': True,
                'message': 'Projects retrieved successfully',
                'data': serializer.data,
                'count': queryset.count()
            },
            status=status.HTTP_200_OK
        )
    
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific project."""
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            
            return Response(
                {
                    'success': True,
                    'message': 'Project retrieved successfully',
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Project.DoesNotExist:
            return Response(
                {
                    'success': False,
                    'message': 'Project not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """Update a project."""
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response(
                {
                    'success': True,
                    'message': 'Project updated successfully',
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
    
    def destroy(self, request, *args, **kwargs):
        """Delete a project."""
        try:
            instance = self.get_object()
            instance.delete()
            
            return Response(
                {
                    'success': True,
                    'message': 'Project deleted successfully'
                },
                status=status.HTTP_204_NO_CONTENT
            )
        except Project.DoesNotExist:
            return Response(
                {
                    'success': False,
                    'message': 'Project not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Update project status."""
        try:
            project = self.get_object()
            new_status = request.data.get('status')
            
            if not new_status:
                return Response(
                    {
                        'success': False,
                        'message': 'Status is required'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            updated_project = ProjectService.update_project_status(pk, new_status)
            serializer = self.get_serializer(updated_project)
            
            return Response(
                {
                    'success': True,
                    'message': 'Project status updated successfully',
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'success': False,
                    'message': 'Failed to update project status',
                    'errors': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
