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
        user = User.objects.create(
            email=validated_data["email"], name=validated_data["name"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
