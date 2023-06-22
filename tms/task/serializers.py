from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "description",
            "completed",
            "due_date",
            "priority",
            "assignee",
            "created_at",
            "updated_at",
            "created_by",
        ]
