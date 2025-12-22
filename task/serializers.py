from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model with project name included."""
    project_name = serializers.CharField(source='project.title', read_only=True)
    project_owner = serializers.CharField(source='project.owner.username', read_only=True)
    
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class TaskCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating tasks."""
    class Meta:
        model = Task
        fields = ('title', 'description', 'project', 'status', 'priority', 'due_date')
        
    def validate_project(self, value):
        """Ensure the project exists and user has access."""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            if value.owner != request.user:
                raise serializers.ValidationError(
                    "You don't have permission to create tasks in this project."
                )
        return value