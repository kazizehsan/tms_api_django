from rest_framework import serializers

from django.contrib.auth.models import Group

from task.serializers import TaskSerializer
from .models import User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]


class UserSerializer(serializers.ModelSerializer):
    assigned_tasks = TaskSerializer(many=True, read_only=True)
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "name", "password", "assigned_tasks", "groups"]
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


class UserGroupUpdateRequestSerializer(serializers.Serializer):
    groups = serializers.ListField(child=serializers.IntegerField())
