from rest_framework import serializers

from task.serializers import TaskSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    assigned_tasks = TaskSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = ["id", "email", "name", "password", "assigned_tasks"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        # Remove relationship if any
        # example_relationship = validated_data.pop('example_relationship')
        user = User.objects.create(
            email=validated_data["email"], name=validated_data["name"]
        )
        # Add the relationship after the instance is created
        # user.example_relationship = example_relationship
        user.set_password(validated_data["password"])
        user.save()
        return user
